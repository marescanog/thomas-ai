import base64
import io
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import numpy as np

# Import your helper from yolo.py that returns detections.
from .yolo import classify_image

# Later in the view, when you need to access the inventory data:
from inventory.models import Products

def decode_image_from_data_url(data_url):
    """
    Given a data URL (Base64 encoded image), decode it to a NumPy array.
    """
    header, encoded = data_url.split(',', 1)
    data = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(data)).convert('RGB')
    return np.array(image)

@csrf_exempt
def classify(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data_url = data.get('image')
            if not image_data_url:
                return JsonResponse({'error': 'No image provided'}, status=400)

            # Decode the image from the POSTed data
            image = decode_image_from_data_url(image_data_url)

            # Run inference using your YOLOv8 model helper
            detections = classify_image(image)
            # Example detection format:
            # detections = [
            #   {'class': '0', 'confidence': 0.85, 'box': [...]},
            #   {'class': '1', 'confidence': 0.80, 'box': [...]},
            #   {'class': '2', 'confidence': 0.90, 'box': [...]},
            # edit
            # ]

            # Deduplicate: keep only one detection per class (the one with the highest confidence)
            unique_detections = {}
            for detection in detections:
                label = detection.get("class")
                conf = detection.get("confidence", 0)
                # If this class hasn't been seen, or if the new detection has a higher confidence, update it.
                if label not in unique_detections or conf > unique_detections[label]["confidence"]:
                    unique_detections[label] = detection

            # Convert the unique detections into a list.
            unique_detection_list = list(unique_detections.values())

            # Determine which detection has the highest overall confidence (if any)
            if unique_detection_list:
                highest_detection = max(unique_detection_list, key=lambda d: d["confidence"])
            else:
                highest_detection = None

            # Query the inventory database for the product details based on the highest confidence detection
            highest_product_info = {}
            if highest_detection:
                product = Products.objects.filter(
                    class_label_name__iexact=highest_detection["class"]
                ).first()
                if product:
                    highest_product_info = {
                        "product_id": product.product_id,
                        "product_name": product.product_name,
                        "class_label_name": product.class_label_name,
                        "product_type": product.product_type,
                        "alcohol_volume": product.alcohol_volume,
                        "category": product.product_type,  # Adjust as needed
                    }

            if highest_detection:
                print("Highest detection class:", highest_detection["class"])

            # Prepare the final response: if there are no detections, return None for all keys.
            if not unique_detection_list:
                response_data = {
                    "detected": None,
                    "highest_score": None,
                    "raw_detections": None,
                }
            else:
                response_data = {
                    "detected": list(unique_detections.keys()),
                    "highest_score": highest_product_info if highest_product_info else None,
                    "raw_detections": unique_detection_list,
                }

            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=400)

