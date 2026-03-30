# Project Overview: Time Shift (Grandpa's Photo Tool)
This repository contains a full-stack web application designed to align and colorize historical sepia/black-and-white photos to match modern reference photos. The end goal is to provide an easy-to-use, single-page web interface with a "Then and Now" slider.

## Tech Stack
* **Backend:** Python 3, FastAPI, Uvicorn
* **Computer Vision & AI:** OpenCV (`cv2`), NumPy
* **Frontend:** HTML, CSS, Vanilla JavaScript (Generated via Google Stitch)

## Agent Directives & Coding Standards

### 1. Backend & Routing (FastAPI)
* Keep the server lightweight. Serve static frontend files directly from a `/static` or `/public` directory.
* Ensure the `/process` endpoint handles file uploads asynchronously and returns clear JSON error messages if image processing fails.
* Do not install heavy ML frameworks like PyTorch or TensorFlow. Rely strictly on `opencv-python` and its `dnn` module for colorization to keep the server easy to host locally.

### 2. Computer Vision Logic (OpenCV)
* **Alignment (Homography):** Use ORB (`cv2.ORB_create()`) for keypoint detection. Use `cv2.BFMatcher` to match features. 
* **Crucial Rule for Alignment:** Historical photos can be blurry. If the homography matrix calculation fails due to insufficient good matches, **do not crash the server**. Catch the exception, bypass the warping step, and return the unaligned (but still colorized) photo to the frontend with a warning flag.
* **Colorization:** Use the Zhang Caffe model via `cv2.dnn`. Ensure you handle the LAB color space conversions carefully, scaling the L channel correctly before merging the predicted a and b channels.

### 3. Frontend Integration
* Maintain the UI structure provided by Stitch.
* Keep JavaScript vanilla. Do not introduce React, Vue, or heavy state management libraries.
* Ensure the slider logic updates dynamically based on mouse/touch drag events. 
* Always display the loading state while the FastAPI server is processing the images.

### 4. Communication
* When opening a Pull Request, briefly explain any complex OpenCV math or matrix transformations you implemented so the human reviewer can understand the image manipulation pipeline.
