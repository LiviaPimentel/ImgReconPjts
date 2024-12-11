# Motion Detection Scripts

This repository contains two Python scripts for motion detection using OpenCV. These scripts are designed to detect movement in video streams or from a webcam feed by processing frames, identifying changes, and marking detected regions.

---

## Script 1: Basic Motion Detection with Contours

### Features
- Captures live video feed using a webcam.
- Detects motion by calculating frame differences.
- Identifies contours of moving objects and draws bounding boxes.
- Displays a real-time video feed with highlighted motion regions.
- Quits on pressing the `q` key.

### Usage
1. Install the required dependencies: pip install opencv-python numpy

2. Run the script in your Python environment:
```bash
python motion_detection_basic.py
```

### Output: A live video feed with motion highlighted using green bounding boxes.
