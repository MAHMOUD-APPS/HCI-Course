# os: provides functions for interacting with the operating system (file paths, directories)
import os
# cv2: OpenCV library — the core library for computer vision and image processing
import cv2
# numpy: numerical computing library — used here for creating and manipulating image arrays
import numpy as np
# matplotlib.pyplot: plotting library — used to display processed images in a figure window
import matplotlib.pyplot as plt

# Constants defining the folder names for input images and output results
IMAGES_DIR = "images"
OUTPUT_DIR = "output"


# ──────────────────────────────────────────────
# Mode 1: Live Video Feed from Webcam
# Captures live video, converts color space,
# and draws an overlay rectangle + quit instruction
# ──────────────────────────────────────────────
def video_feed():
    # Open a connection to the default webcam (index 0 = first camera)
    cap = cv2.VideoCapture(index=0)

    while True:
        # Read one frame from the webcam; ret is True if the frame was captured successfully
        ret, frame = cap.read()

        # Convert the frame from BGR (OpenCV default) to RGB for correct color display
        frame = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2RGB)

        # Draw a green rectangle on the frame from top-left (50,50) to bottom-right (200,200)
        cv2.rectangle(img=frame, pt1=(50, 50), pt2=(200, 200), color=(0, 255, 0), thickness=8)

        # Overlay instruction text on the frame so the user knows how to exit
        cv2.putText(img=frame, text="Press 'q' to quit", org=(50, 40),
                     fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                     color=(0, 255, 0), thickness=2)

        # Display the processed frame in a window titled "Video Feed"
        cv2.imshow(winname="Video Feed", mat=frame)

        # Wait 1 ms for a key press; if 'q' is pressed, break out of the loop
        if cv2.waitKey(delay=1) & 0xFF == ord('q'):
            break

    # Release the webcam so other applications can use it
    cap.release()
    # Close all OpenCV windows
    cv2.destroyAllWindows()


# ──────────────────────────────────────────────
# Mode 2: Pupil / Iris Detection on Static Images
# Reads eye images, applies grayscale + thresholding
# to isolate the dark pupil, finds contours, and
# saves/displays the contour overlay
# ──────────────────────────────────────────────
def detect_eyes():
    # Create the output directory if it doesn't already exist
    os.makedirs(name=OUTPUT_DIR, exist_ok=True)

    # Define the image file extensions we support
    supported_ext = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

    # List all supported image files in the images folder, sorted alphabetically
    files = sorted(
        f for f in os.listdir(IMAGES_DIR)
        if f.lower().endswith(supported_ext)
    )

    # If no images were found, notify the user and exit early
    if not files:
        print(f"No images found in '{IMAGES_DIR}/'")
        return

    print(f"Found {len(files)} image(s) in '{IMAGES_DIR}/'")

    # ── Processing loop: iterate over each image file ──
    for filename in files:
        # Build the full path to the input image
        input_path = os.path.join(IMAGES_DIR, filename)

        # Load the image from disk as a BGR NumPy array
        eye_img = cv2.imread(filename=input_path)

        # Skip files that could not be read (corrupted or unsupported)
        if eye_img is None:
            print(f"  [SKIP] Could not read: {filename}")
            continue

        # Convert the color image to grayscale (single channel) for thresholding
        eye_gray = cv2.cvtColor(src=eye_img, code=cv2.COLOR_BGR2GRAY)

        # Apply inverse binary thresholding:
        #   pixels darker than 30 become white (255) — these are the pupil
        #   pixels brighter than 30 become black (0)  — these are the iris/sclera
        _, thresh = cv2.threshold(src=eye_gray, thresh=30, maxval=255, type=cv2.THRESH_BINARY_INV)

        # Find the outer contours (boundaries) of the white regions in the thresholded image
        #   RETR_EXTERNAL  = only outermost contours (ignores nested holes)
        #   CHAIN_APPROX_SIMPLE = compress contour points to save memory
        contours, _ = cv2.findContours(image=thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

        # Create a blank black image with the same dimensions as the original
        contour_image = np.zeros_like(a=eye_img, dtype=np.uint8)

        # Draw all detected contours (contourIdx=-1) in green on the blank image
        cv2.drawContours(image=contour_image, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2)

        # Build the output file path: e.g. "output/eye1_contour.jpg"
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(OUTPUT_DIR, f"{name}_contour.jpg")

        # Save the contour image to disk
        cv2.imwrite(filename=output_path, img=contour_image)
        print(f"  [OK] {filename} -> {output_path}")

    print(f"\nAll results saved to '{OUTPUT_DIR}/'")
    print("Displaying results...")

    # ── Display loop: show each saved contour image using matplotlib ──
    for filename in files:
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(OUTPUT_DIR, f"{name}_contour.jpg")

        # Load the saved contour image
        result = cv2.imread(filename=output_path)

        if result is not None:
            # Create a new figure with a width of 8 inches and height of 6 inches
            plt.figure(figsize=(8, 6))

            # Convert BGR to RGB before displaying (matplotlib expects RGB)
            plt.imshow(X=cv2.cvtColor(src=result, code=cv2.COLOR_BGR2RGB))

            # Set the figure title to the original filename
            plt.title(label=f"{filename}")

            # Hide the axis ticks and labels for a cleaner look
            plt.axis("off")

    # Render and show all matplotlib figures at once
    plt.show()


# ──────────────────────────────────────────────
# Mode 3: Real-Time Face & Eye Detection
# Uses Haar cascade classifiers to detect faces
# and eyes in a live webcam stream, drawing
# bounding boxes around each detection
# ──────────────────────────────────────────────
def face_detection():
    # Load the pre-trained Haar cascade XML for frontal face detection
    face_cascade = cv2.CascadeClassifier(filename=cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Load the pre-trained Haar cascade XML for eye detection
    eye_cascade = cv2.CascadeClassifier(filename=cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Open the default webcam
    cap = cv2.VideoCapture(index=0)

    while True:
        # Capture a single frame from the webcam
        ret, frame = cap.read()

        # Convert to grayscale — Haar classifiers only work on single-channel images
        gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale image
        #   scaleFactor=1.3  — shrink image by 30% at each scale (multi-scale detection)
        #   minNeighbors=5   — require 5 overlapping detections to confirm a face (reduces false positives)
        faces = face_cascade.detectMultiScale(image=gray, scaleFactor=1.3, minNeighbors=5)

        # Loop over each detected face bounding box (x, y, width, height)
        for (x, y, w, h) in faces:
            # Draw a blue rectangle around the detected face
            cv2.rectangle(img=frame, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)

            # Extract the face region of interest (ROI) from the grayscale image
            roi_gray = gray[y:y+h, x:x+w]

            # Extract the face ROI from the color image (for drawing eye rectangles)
            roi_color = frame[y:y+h, x:x+w]

            # Detect eyes only within the face ROI (narrows the search area)
            eyes = eye_cascade.detectMultiScale(image=roi_gray)

            # Loop over each detected eye bounding box
            for (ex, ey, ew, eh) in eyes:
                # Draw a green rectangle around each detected eye
                cv2.rectangle(img=roi_color, pt1=(ex, ey), pt2=(ex + ew, ey + eh), color=(0, 255, 0), thickness=2)

                # Show quit instruction on the frame
                cv2.putText(img=frame, text="Press 'q' to quit", org=(50, 40),
                             fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                             color=(0, 255, 0), thickness=2)

        # Display the annotated frame in a window
        cv2.imshow(winname='Face Detection', mat=frame)

        # Wait 1 ms for a key press; exit on 'q'
        if cv2.waitKey(delay=1) & 0xFF == ord('q'):
            break

    # Release the webcam
    cap.release()
    # Close all OpenCV display windows
    cv2.destroyAllWindows()


# ──────────────────────────────────────────────
# Entry point: show a menu and run the selected mode
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("Eye Tracking - HCI Project")
    print("-" * 30)
    print("1. Video Feed")
    print("2. Pupil/Iris Detection")
    print("3. Face & Eye Detection")
    print("-" * 30)

    # Prompt the user to pick a mode and strip any leading/trailing whitespace
    choice = input("Select mode (1-3): ").strip()

    if choice == "1":
        video_feed()
    elif choice == "2":
        detect_eyes()
    elif choice == "3":
        face_detection()
    else:
        print("Invalid choice. Please run again and select 1, 2, or 3.")
