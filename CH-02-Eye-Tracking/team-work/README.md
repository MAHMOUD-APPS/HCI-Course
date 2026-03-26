# Eye Tracking using OpenCV

**Course:** Human-Computer Interaction (HCI)
**Program:** Master's Degree, Second Semester
**University:** Helwan University
**Supervisor:** Dr. Sayed

## Overview

This project demonstrates fundamental eye tracking and face detection techniques using computer vision. It showcases three core capabilities relevant to HCI research:

1. **Live Video Feed** — Captures webcam input and renders an overlay region of interest (ROI).
2. **Pupil/Iris Detection** — Applies grayscale conversion, binary thresholding, and contour extraction on a static eye image to isolate the pupil region.
3. **Real-Time Face & Eye Detection** — Uses Haar cascade classifiers to detect faces and eyes from a live webcam stream in real time.

## Prerequisites

- Python 3.12+
- A working webcam (for live detection modes)
- An eye image file named `eye_sample.jpg` in the project root (for static pupil detection)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd presentation
```

### 2. Create a virtual environment

**macOS / Linux:**

```bash
python3 -m venv venv
```

**Windows:**

```cmd
python -m venv venv
```

### 3. Activate the virtual environment

**macOS / Linux:**

```bash
source venv/bin/activate
```

**Windows (Command Prompt):**

```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

> After activation you should see `(venv)` at the beginning of your terminal prompt.

### 4. Install dependencies

```bash
pip install opencv-python numpy matplotlib
```

### Deactivating the virtual environment

When you're done, run:

```bash
deactivate
```

## Usage

Run the script:

```bash
python eye_tracking.py
```

You will see an interactive menu:

```
Eye Tracking - HCI Project
------------------------------
1. Video Feed
2. Pupil/Iris Detection
3. Face & Eye Detection
------------------------------
Select mode (1-3):
```

Enter `1`, `2`, or `3` to launch the corresponding mode. Press **`q`** to quit the webcam window.

### Modes

| # | Mode | Description |
|---|---|---|
| 1 | Video Feed | Opens the webcam and displays a raw feed with a green ROI rectangle |
| 2 | Pupil/Iris Detection | Loads `eye_sample.jpg`, applies thresholding and contour detection to locate the pupil, and displays the result |
| 3 | Face & Eye Detection | Detects faces (blue boxes) and eyes (green boxes) in real time using Haar cascades |

## How It Works

### Face & Eye Detection Pipeline

```
Webcam Frame
    │
    ▼
Grayscale Conversion (cv2.cvtColor)
    │
    ▼
Haar Cascade – Face Detection (haarcascade_frontalface_default.xml)
    │
    ▼
Region of Interest (ROI) Extraction
    │
    ▼
Haar Cascade – Eye Detection (haarcascade_eye.xml)
    │
    ▼
Bounding Box Overlay → Display
```

### Pupil Detection Pipeline

```
Static Eye Image (eye_sample.jpg)
    │
    ▼
Grayscale Conversion
    │
    ▼
Binary Inverse Thresholding (threshold = 30)
    │
    ▼
Contour Detection (cv2.findContours)
    │
    ▼
Contour Visualization → Save & Display
```

## Dependencies

| Package | Purpose |
|---|---|
| `opencv-python` | Image processing, video capture, Haar cascade classifiers |
| `numpy` | Array operations for image manipulation |
| `matplotlib` | Visualization of processed images |

## Project Structure

```
presentation/
├── eye_tracking.py    # Main script with all detection functions
├── eye_sample.jpg              # Sample eye image for pupil detection
├── contour_image.jpg  # Generated output from detect_eyes()
├── venv/              # Python virtual environment
└── README.md
```

## References

- Viola, P., & Jones, M. (2001). *Rapid Object Detection using a Boosted Cascade of Simple Features.* IEEE CVPR.
- OpenCV Haar Cascades Documentation: https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html
- Timm, F., & Barth, E. (2011). *Accurate Eye Centre Localisation by Means of Gradients.* VISAPP.
