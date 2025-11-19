# Football Player Detection App

A web application that detects football players in match screenshots and videos using YOLOv8 object detection. Upload or paste an image, or upload a video, and the app will identify all players on the field with bounding boxes and confidence scores.

## Features

### Image Mode
- **Image Upload**: Upload football match screenshots via file selection or drag-and-drop
- **Paste Support**: Paste images directly from clipboard (Ctrl+V / Cmd+V)
- **Player Detection**: Automatically detects all players (people) in images
- **Instant Results**: Fast processing for single images

### Video Mode
- **Video Upload**: Upload football match videos in multiple formats (MP4, AVI, MOV, MKV, FLV, WMV, WebM)
- **Frame-by-Frame Detection**: Processes each frame with player detection
- **Annotated Output**: Generates a new video with bounding boxes on all detected players
- **Video Download**: Download the processed video with all annotations
- **Statistics**: View total detections, frame count, and average detections per frame

### Common Features
- **Bounding Boxes**: Draws green boxes around each detected player
- **Confidence Scores**: Displays confidence percentage for each detection
- **Adjustable Threshold**: Control detection sensitivity with a slider (0.1 - 0.9)
- **Modern UI**: Beautiful, responsive web interface with dual-mode support

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Object Detection**: YOLOv8 (Ultralytics)
- **Image/Video Processing**: OpenCV, Pillow
- **Frontend**: HTML, CSS, JavaScript
- **Video Codec**: MP4V (MPEG-4)

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

2. **Select Mode**: Choose between Image Mode or Video Mode

#### Image Mode

3. **Upload an image** using one of these methods:
   - Click "Choose File" button
   - Drag and drop an image onto the upload area
   - Copy an image to clipboard and press Ctrl+V (or Cmd+V on Mac)

4. **Adjust confidence threshold** (optional)
   - Use the slider to set the minimum confidence for detection (0.1 to 0.9)
   - Default is 0.30 (30%)
   - Higher values = fewer, more confident detections
   - Lower values = more detections, possibly including false positives

5. **Click "Detect Players"**
   - The app will process the image and detect all players
   - Results appear below with:
     - Total player count
     - Annotated image with bounding boxes
     - List of detections with confidence percentages

#### Video Mode

3. **Upload a video**:
   - Click "Choose File" button to select a video file
   - Supported formats: MP4, AVI, MOV, MKV, FLV, WMV, WebM
   - Maximum file size: 500MB

4. **Adjust confidence threshold** (optional)
   - Same as image mode

5. **Click "Detect Players"**
   - The app will process each frame of the video
   - Processing time depends on video length and resolution
   - A typical 30-second video may take 1-3 minutes to process

6. **View and Download Results**:
   - Processed video plays in the browser with all bounding boxes
   - Statistics shown:
     - Total detections across all frames
     - Total number of frames
     - Average detections per frame
   - Click "Download Processed Video" to save the annotated video

## How It Works

### Image Processing
1. **Image Input**: User uploads or pastes a football match screenshot
2. **Object Detection**: YOLOv8 model analyzes the image and detects all people
3. **Filtering**: Only "person" class detections are considered as players
4. **Annotation**: Green bounding boxes are drawn around each player
5. **Confidence Display**: Each detection shows its confidence score
6. **Results**: Annotated image and detection statistics are displayed

### Video Processing
1. **Video Input**: User uploads a video file
2. **Frame Extraction**: Video is processed frame by frame
3. **Per-Frame Detection**: YOLOv8 analyzes each frame individually
4. **Real-time Annotation**: Bounding boxes are drawn on each frame
5. **Video Reconstruction**: Annotated frames are reassembled into an output video
6. **Download**: Processed video is made available for download

## Project Structure

```
first_repo/
├── app.py                          # Main Flask application with video support
├── requirements.txt                # Python dependencies
├── templates/
│   └── index.html                 # Web interface with dual-mode support
├── static/
│   └── outputs/                   # Processed videos (auto-created)
│       └── .gitkeep              # Keeps directory in git
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

If you encounter memory issues with large images or videos:
1. Resize images/videos before upload
2. Use a smaller model (yolov8n.pt) - already default
3. Increase system memory
4. For videos, reduce resolution or trim to shorter clips

### Video Processing Issues

**Slow processing**:
- Video processing is CPU/GPU intensive
- Expected: ~2-5 seconds per second of video on typical hardware
- Consider using shorter clips for testing

**Video won't play in browser**:
- Try downloading and playing in VLC or another media player
- Some browsers may not support the MP4V codec
- The file is still valid and downloadable

**Large output files**:
- Output video size depends on input resolution and length
- Consider compressing the input video first
- Processed videos are saved in `static/outputs/` directory

## Examples

### Images
Try the app with:
- Football match screenshots from TV broadcasts
- Stadium photos from sports websites
- Training session photos
- Match highlights screenshots

### Videos
Try the app with:
- Short match highlight clips (10-60 seconds recommended)
- Training session recordings
- Goal replays
- Corner kick or free kick footage
- Keep videos under 2 minutes for faster processing

## Future Enhancements

Possible improvements:
- Team classification (detect and separate teams by jersey color)
- Player tracking across video frames with unique IDs
- Ball detection and tracking
- Formation analysis and tactical insights
- Heatmap generation showing player movement
- Multiple image batch processing
- Real-time video processing with live streaming
- Export to different video formats (H.264, H.265)
- Progress bar for video processing
- Player number recognition (OCR)

## License

This project uses open-source libraries:
- Flask: BSD License
- Ultralytics YOLOv8: AGPL-3.0 License
- OpenCV: Apache 2.0 License

## Support

For issues or questions about this application, please refer to the documentation of the respective libraries or open an issue in the project repository.
