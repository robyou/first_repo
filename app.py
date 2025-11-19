import os
import base64
import io
from flask import Flask, render_template, request, jsonify
from PIL import Image
import cv2
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 36 * 1024 * 1024  # 36MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load YOLO model (using YOLOv8 pre-trained on COCO dataset)
# The model will be downloaded automatically on first run
model = YOLO('yolov8x.pt')  # Using nano model for faster inference

def detect_players(image_path, confidence_threshold=0.3):
    """
    Detect players (people) in the image and draw bounding boxes.

    Args:
        image_path: Path to the input image
        confidence_threshold: Minimum confidence score for detection

    Returns:
        Annotated image as base64 string and detection info
    """
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image")

    # Run inference
    results = model(img, conf=confidence_threshold)

    # Get detections
    detections = []

    # Process results
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Get box coordinates
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

            # Get confidence and class
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            # Filter for person class (class_id 0 in COCO dataset)
            if class_id == 0:  # Person class
                # Draw bounding box
                color = (0, 255, 0)  # Green color
                thickness = 2
                cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)

                # Draw confidence label
                label = f'Player: {confidence:.2f}'
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.6
                font_thickness = 2

                # Get text size for background
                (text_width, text_height), baseline = cv2.getTextSize(label, font, font_scale, font_thickness)

                # Draw background rectangle for text
                cv2.rectangle(img,
                            (int(x1), int(y1) - text_height - 10),
                            (int(x1) + text_width, int(y1)),
                            color,
                            -1)

                # Draw text
                cv2.putText(img, label, (int(x1), int(y1) - 5),
                           font, font_scale, (0, 0, 0), font_thickness)

                # Store detection info
                detections.append({
                    'bbox': [int(x1), int(y1), int(x2), int(y2)],
                    'confidence': confidence,
                    'class': class_name
                })

    # Convert image to base64 for web display
    _, buffer = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    return img_base64, detections

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    """Handle image upload and perform player detection."""
    try:
        # Check if image is uploaded or pasted
        if 'file' in request.files and request.files['file'].filename != '':
            # Handle file upload
            file = request.files['file']

            # Save uploaded file
            filename = 'uploaded_image.jpg'
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

        elif 'image_data' in request.form:
            # Handle pasted image (base64)
            image_data = request.form['image_data']

            # Remove data URL prefix if present
            if 'base64,' in image_data:
                image_data = image_data.split('base64,')[1]

            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))

            # Save image
            filename = 'pasted_image.jpg'
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
        else:
            return jsonify({'error': 'No image provided'}), 400

        # Get confidence threshold from request (default 0.3)
        confidence_threshold = float(request.form.get('confidence', 0.3))

        # Perform detection
        img_base64, detections = detect_players(filepath, confidence_threshold)

        # Return results
        return jsonify({
            'success': True,
            'image': img_base64,
            'detections': detections,
            'total_players': len(detections)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Football Player Detection App...")
    print("Open your browser and go to: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
