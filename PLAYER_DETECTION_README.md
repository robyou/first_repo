# Football Player Detection App

A simple web application that detects football players in match screenshots using YOLOv8 object detection. Upload or paste an image, and the app will identify all players on the field with bounding boxes and confidence scores.

## Features

- **Image Upload**: Upload football match screenshots via file selection or drag-and-drop
- **Paste Support**: Paste images directly from clipboard (Ctrl+V / Cmd+V)
- **Player Detection**: Automatically detects all players (people) in the image
- **Bounding Boxes**: Draws green boxes around each detected player
- **Confidence Scores**: Displays confidence percentage for each detection
- **Adjustable Threshold**: Control detection sensitivity with a slider
- **Modern UI**: Beautiful, responsive web interface

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Object Detection**: YOLOv8 (Ultralytics)
- **Image Processing**: OpenCV, Pillow
- **Frontend**: HTML, CSS, JavaScript

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the repository**
   ```bash
   cd /home/user/first_repo
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - Flask 3.0.0
   - Ultralytics 8.1.0 (YOLOv8)
   - OpenCV 4.8.1.78
   - Pillow 10.1.0
   - NumPy 1.24.3

3. **First Run (Model Download)**

   On the first run, YOLOv8 will automatically download the pre-trained model (`yolov8n.pt`). This is a one-time download of approximately 6MB.

## Usage

### Starting the Application

Run the Flask application:

```bash
python app.py
```

You should see:
```
Starting Football Player Detection App...
Open your browser and go to: http://localhost:5000
```

### Using the Web Interface

1. **Open your browser** and navigate to `http://localhost:5000`

2. **Upload an image** using one of these methods:
   - Click "Choose File" button
   - Drag and drop an image onto the upload area
   - Copy an image to clipboard and press Ctrl+V (or Cmd+V on Mac)

3. **Adjust confidence threshold** (optional)
   - Use the slider to set the minimum confidence for detection (0.1 to 0.9)
   - Default is 0.30 (30%)
   - Higher values = fewer, more confident detections
   - Lower values = more detections, possibly including false positives

4. **Click "Detect Players"**
   - The app will process the image and detect all players
   - Results appear below with:
     - Total player count
     - Annotated image with bounding boxes
     - List of detections with confidence percentages

## How It Works

1. **Image Input**: User uploads or pastes a football match screenshot
2. **Object Detection**: YOLOv8 model analyzes the image and detects all people
3. **Filtering**: Only "person" class detections are considered as players
4. **Annotation**: Green bounding boxes are drawn around each player
5. **Confidence Display**: Each detection shows its confidence score
6. **Results**: Annotated image and detection statistics are displayed

## Project Structure

```
first_repo/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── templates/
│   └── index.html                 # Web interface
├── uploads/                       # Temporary upload folder (auto-created)
└── PLAYER_DETECTION_README.md     # This file
```

## Configuration

### Confidence Threshold

The confidence threshold determines how certain the model must be to report a detection:

- **Low (0.1-0.3)**: More detections, including uncertain ones
- **Medium (0.3-0.5)**: Balanced (recommended)
- **High (0.5-0.9)**: Only very confident detections

### Model Selection

By default, the app uses `yolov8n.pt` (nano model) for faster inference. You can change to a more accurate model in `app.py`:

```python
model = YOLO('yolov8n.pt')  # Options: yolov8n, yolov8s, yolov8m, yolov8l, yolov8x
```

Models from smallest/fastest to largest/most accurate:
- `yolov8n.pt` - Nano (6MB) - Fastest
- `yolov8s.pt` - Small (22MB)
- `yolov8m.pt` - Medium (52MB)
- `yolov8l.pt` - Large (88MB)
- `yolov8x.pt` - Extra Large (136MB) - Most Accurate

## Limitations

- The model detects "people" in general, not specifically football players
- Performance depends on:
  - Image quality and resolution
  - Player visibility and occlusion
  - Lighting conditions
  - Distance of players from camera
- May detect referees, coaches, and other people on or near the field
- Small or partially occluded players may not be detected

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, change it in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### Model Download Issues

If the model fails to download automatically:
1. Download manually from: https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
2. Place it in the project directory
3. Update the model path in `app.py`

### Memory Issues

If you encounter memory issues with large images:
1. Resize images before upload
2. Use a smaller model (yolov8n.pt)
3. Increase system memory

## Examples

Try the app with:
- Football match screenshots from TV broadcasts
- Stadium photos from sports websites
- Training session photos
- Match highlights screenshots

## Future Enhancements

Possible improvements:
- Team classification (detect and separate teams by jersey color)
- Player tracking across video frames
- Ball detection
- Formation analysis
- Heatmap generation
- Multiple image batch processing

## License

This project uses open-source libraries:
- Flask: BSD License
- Ultralytics YOLOv8: AGPL-3.0 License
- OpenCV: Apache 2.0 License

## Support

For issues or questions about this application, please refer to the documentation of the respective libraries or open an issue in the project repository.
