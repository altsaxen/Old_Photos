# Project Overview: Time Shift (Core Features MVP)
This repository contains a lightweight, full-stack web application designed to align and colorize historical photos. The UI contains four tabs, but we are currently ONLY implementing the backend logic for two: "Time Shift" and "Colorization".

## Tech Stack
* **Backend:** Python 3, FastAPI, Uvicorn
* **Computer Vision & AI:** OpenCV (`cv2`), NumPy
* **Frontend:** HTML, CSS, Vanilla JavaScript (Generated via Google Stitch)

## Agent Directives & Coding Standards

### 1. Backend & Routing (FastAPI)
* Serve static frontend files directly from the root or a `/static` directory.
* Create distinct API endpoints for the active features (e.g., `/api/align` and `/api/colorize`).
* Do not install heavy ML frameworks like PyTorch. Rely strictly on `opencv-python` and its `dnn` module to keep the server easy to host locally.
* For the "Enhancement" and "Batch Process" UI tabs, simply log a "Feature coming soon" message to the console; do not build backend logic for them yet.

### 2. Computer Vision Logic (OpenCV)
* **Alignment (Time Shift):** Use ORB (`cv2.ORB_create()`) and `cv2.BFMatcher` to find the Homography matrix. **Crucial:** If homography fails due to a lack of good matches (common in blurry old photos), catch the exception, bypass the warping step, and return the original unaligned photo with an error flag so the server doesn't crash.
* **Colorization:** Use the Zhang Caffe model via `cv2.dnn`. Handle LAB color space conversions carefully.

### 3. Frontend Integration
* Keep JavaScript vanilla.
* Ensure the slider logic on the Time Shift tab updates dynamically when the user drags it.
* Always display a loading state while FastAPI processes images.
