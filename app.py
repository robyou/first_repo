import os
import base64
import io
import time
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
from PIL import Image
import cv2
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size for videos
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'static/outputs'

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

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

def detect_players_video(video_path, confidence_threshold=0.3, progress_callback=None):
    """
    Detect players (people) in a video and draw bounding boxes.

    Args:
        video_path: Path to the input video
        confidence_threshold: Minimum confidence score for detection
        progress_callback: Optional callback function for progress updates

    Returns:
        Path to the output video and total detections
    """
    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Could not open video file")

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create output video path
    timestamp = int(time.time())
    output_filename = f'output_video_{timestamp}.mp4'
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    # Define codec and create VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    total_detections = 0

    # Process each frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run inference on frame
        results = model(frame, conf=confidence_threshold, verbose=False)

        # Process results
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get box coordinates
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

                # Get confidence and class
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])

                # Filter for person class (class_id 0 in COCO dataset)
                if class_id == 0:  # Person class
                    total_detections += 1

                    # Draw bounding box
                    color = (0, 255, 0)  # Green color
                    thickness = 2
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)

                    # Draw confidence label
                    label = f'Player: {confidence:.2f}'
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.6
                    font_thickness = 2

                    # Get text size for background
                    (text_width, text_height), baseline = cv2.getTextSize(label, font, font_scale, font_thickness)

                    # Draw background rectangle for text
                    cv2.rectangle(frame,
                                (int(x1), int(y1) - text_height - 10),
                                (int(x1) + text_width, int(y1)),
                                color,
                                -1)

                    # Draw text
                    cv2.putText(frame, label, (int(x1), int(y1) - 5),
                               font, font_scale, (0, 0, 0), font_thickness)

        # Write processed frame
        out.write(frame)
        frame_count += 1

        # Report progress
        if progress_callback and frame_count % 10 == 0:
            progress = int((frame_count / total_frames) * 100)
            progress_callback(progress)

    # Release everything
    cap.release()
    out.release()

    return output_filename, total_detections, total_frames

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

@app.route('/detect_video', methods=['POST'])
def detect_video():
    """Handle video upload and perform player detection."""
    try:
        # Check if video is uploaded
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({'error': 'No video file provided'}), 400

        file = request.files['file']

        # Validate file extension
        allowed_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            return jsonify({'error': f'Unsupported video format. Allowed: {", ".join(allowed_extensions)}'}), 400

        # Save uploaded video
        timestamp = int(time.time())
        filename = f'uploaded_video_{timestamp}{file_ext}'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Get confidence threshold from request (default 0.3)
        confidence_threshold = float(request.form.get('confidence', 0.3))

        # Perform video detection
        output_filename, total_detections, total_frames = detect_players_video(
            filepath,
            confidence_threshold
        )

        # Return results
        return jsonify({
            'success': True,
            'video_url': f'/outputs/{output_filename}',
            'total_detections': total_detections,
            'total_frames': total_frames,
            'filename': output_filename
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/outputs/<filename>')
def serve_output(filename):
    """Serve processed video files."""
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    print("Starting Football Player Detection App...")
    print("Open your browser and go to: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
