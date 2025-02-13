// static/js/camera.js

// Helper function to get the CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener("DOMContentLoaded", function() {
  const video = document.getElementById('video');

  // Start camera when modal is shown
  $('#cameraModal').on('shown.bs.modal', function () {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
          video.srcObject = stream;
          video.play();
        })
        .catch(function(err) {
          console.error("Error accessing the camera: " + err);
        });
    } else {
      console.error("getUserMedia not supported in this browser.");
    }
  });

  // Stop camera when modal is hidden
  $('#cameraModal').on('hidden.bs.modal', function () {
    const stream = video.srcObject;
    if (stream) {
      let tracks = stream.getTracks();
      tracks.forEach(function(track) {
        track.stop();
      });
      video.srcObject = null;
    }
  });

  // Capture image and send to YOLO inference endpoint
  document.getElementById('captureButton').addEventListener('click', function(){
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageDataURL = canvas.toDataURL('image/png');

    fetch('/classification/classify/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({ image: imageDataURL })
    })
    .then(response => response.json())
    .then(data => {
      console.log("Inference result:", data);

      // Build HTML for the Product Information card
      let productHTML = "";
      if (data.highest_score) {
        productHTML += `<ul>`;
        productHTML += `<li><b>Name:</b> ${data.highest_score.product_name}</li>`;
        productHTML += `<li><b>Category:</b> ${data.highest_score.category}</li>`;
        productHTML += `<li><b>Type:</b> ${data.highest_score.product_type}</li>`;
        productHTML += `<li><b>Alcohol Volume:</b> ${data.highest_score.alcohol_volume}</li>`;
        productHTML += `</ul>`;
      } else {
        productHTML = `<p>No product found!</p>`;
      }
      document.getElementById("productInfoContent").innerHTML = productHTML;

      // If a product was detected, show the additional sections; otherwise, hide them.
      if (data.highest_score) {
        document.getElementById("inventoryRecommendationCard").style.display = "block";
        document.getElementById("salesTrendsCard").style.display = "block";
        document.getElementById("availableProductsCard").style.display = "block";
      } else {
        document.getElementById("inventoryRecommendationCard").style.display = "none";
        document.getElementById("salesTrendsCard").style.display = "none";
        document.getElementById("availableProductsCard").style.display = "none";
      }
    })
    .catch(error => {
      console.error('Error during inference:', error);
    });

    $('#cameraModal').modal('hide');
  });



   // --- Scanning Modal (Real-Time Video Inference) ---
   function getVideoConstraints() {
    // Check if the user agent indicates a mobile device
    const isMobile = /Mobi|Android/i.test(navigator.userAgent);
  
    if (isMobile) {
      // For mobile devices, prefer the back ("environment") camera
      return { video: { facingMode: { ideal: "environment" } } };
    } else {
      // For desktops/laptops, use default video settings (which may select a built-in webcam)
      return { video: true };
    }
  }

   let scanIntervalId = null;
   const scanVideo = document.getElementById('scanVideo');
   const scanCanvas = document.getElementById('scanCanvas');
   const scanCtx = scanCanvas.getContext('2d');
 
   $('#scanModal').on('shown.bs.modal', function () {
     if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
       navigator.mediaDevices.getUserMedia(getVideoConstraints())
         .then(function(stream) {
           scanVideo.srcObject = stream;
           scanVideo.play();
           // Set canvas size to match video dimensions once metadata is loaded
           scanVideo.addEventListener('loadedmetadata', function() {
             scanCanvas.width = scanVideo.videoWidth;
             scanCanvas.height = scanVideo.videoHeight;
           });
           // Start continuous scanning every 1 second
           scanIntervalId = setInterval(() => {
             captureAndScanFrame();
           }, 1000);
         })
         .catch(function(err) {
           console.error("Error accessing the camera for scanning: " + err);
         });
     } else {
       console.error("getUserMedia not supported in this browser.");
     }
   });
 
   $('#scanModal').on('hidden.bs.modal', function () {
     if (scanIntervalId) {
       clearInterval(scanIntervalId);
       scanIntervalId = null;
     }
     const stream = scanVideo.srcObject;
     if (stream) {
       stream.getTracks().forEach(track => track.stop());
       scanVideo.srcObject = null;
     }
     // Clear canvas overlay
     scanCtx.clearRect(0, 0, scanCanvas.width, scanCanvas.height);
   });
 
   function captureAndScanFrame() {
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = scanVideo.videoWidth;
    tempCanvas.height = scanVideo.videoHeight;
    const tempCtx = tempCanvas.getContext('2d');
    tempCtx.drawImage(scanVideo, 0, 0, tempCanvas.width, tempCanvas.height);
    const imageDataURL = tempCanvas.toDataURL('image/png');
  
    fetch('/classification/classify/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({ image: imageDataURL })
    })
    .then(response => response.json())
    .then(data => {
      // Clear previous overlay drawings
      scanCtx.clearRect(0, 0, scanCanvas.width, scanCanvas.height);
      
      if (data.raw_detections && data.raw_detections.length > 0) {
        // Calculate scale factors based on displayed dimensions vs. intrinsic video dimensions.
        const scaleX = scanVideo.offsetWidth / scanVideo.videoWidth;
        const scaleY = scanVideo.offsetHeight / scanVideo.videoHeight;
        
        data.raw_detections.forEach(detection => {
          const box = detection.box; // Assuming format: [x1, y1, x2, y2]
          if (box) {
            // Scale the box coordinates
            const x = box[0] * scaleX;
            const y = box[1] * scaleY;
            const width = (box[2] - box[0]) * scaleX;
            const height = (box[3] - box[1]) * scaleY;
            
            // Draw the bounding box
            scanCtx.strokeStyle = "red";
            scanCtx.lineWidth = 2;
            scanCtx.strokeRect(x, y, width, height);
            
            // Draw the label and confidence above the box
            scanCtx.font = "16px Arial";
            scanCtx.fillStyle = "red";
            const labelText = `${detection.class} (${Math.round(detection.confidence * 100)}%)`;
            scanCtx.fillText(labelText, x, y - 5);
          }
        });
      }
    })
    .catch(error => {
      console.error('Error during scanning inference:', error);
    });
  }
  

});
