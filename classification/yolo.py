# classification/yolo.py
import os
from ultralytics import YOLO
import numpy as np

# Define the path to your model file relative to this file
BASE_MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model')
MODEL_PATH = os.path.join(BASE_MODEL_DIR, 'best.pt')  # or 'last.pt' if desired

# Load the YOLOv8 model
model = YOLO(MODEL_PATH)

# If available, get the class names from the model (a dict mapping indices to labels)
CLASSES = model.names if hasattr(model, 'names') else {}

def classify_image(image):
    """
    Runs YOLOv8 inference on the provided image.
    
    Parameters:
        image (numpy.array): The input image (RGB or BGR depending on your setup).
    
    Returns:
        List[dict]: A list of predictions with bounding boxes, confidences, and class labels.
    """
    # Run inference (YOLOv8 returns a list of Results objects; for a single image, we take the first)
    results = model(image)
    predictions = []

    if results and len(results) > 0:
        result = results[0]  # assuming a single image inference
        boxes = result.boxes  # Contains the detections

        for box in boxes:
            # The following attributes are available for each detection:
            # - box.xyxy: bounding box coordinates in [x1, y1, x2, y2] format
            # - box.conf: confidence score
            # - box.cls: class index
            coords = box.xyxy.cpu().numpy()[0].tolist()  # Convert coordinates to a list
            conf = float(box.conf.cpu().numpy()[0])
            cls_idx = int(box.cls.cpu().numpy()[0])
            label = CLASSES.get(cls_idx, str(cls_idx))  # Map class index to label if available

            predictions.append({
                'box': coords,
                'confidence': conf,
                'class': label,
            })
    return predictions
