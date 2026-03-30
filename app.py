from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
import cv2
import numpy as np
import base64
import urllib.request
from io import BytesIO

app = FastAPI()

# Configuration
PROTO_PATH = "models/colorization_deploy_v2.prototxt"
MODEL_PATH = "models/colorization_release_v2.caffemodel"
HULL_PATH = "models/pts_in_hull.npy"

MODELS_URLS = {
    PROTO_PATH: "https://storage.openvinotoolkit.org/repositories/datumaro/models/colorization/colorization_deploy_v2.prototxt",
    MODEL_PATH: "https://storage.openvinotoolkit.org/repositories/datumaro/models/colorization/colorization_release_v2.caffemodel",
    HULL_PATH: "https://storage.openvinotoolkit.org/repositories/datumaro/models/colorization/pts_in_hull.npy"
}

def ensure_models():
    os.makedirs("models", exist_ok=True)
    for path, url in MODELS_URLS.items():
        if not os.path.exists(path) or os.path.getsize(path) < 1000:
            print(f"Downloading {path} from {url}...")
            urllib.request.urlretrieve(url, path)

# Initial global net variable
net = None

@app.on_event("startup")
async def startup_event():
    global net
    try:
        ensure_models()
        net = cv2.dnn.readNetFromCaffe(PROTO_PATH, MODEL_PATH)
        pts = np.load(HULL_PATH)
        class8 = net.getLayerId("class8_ab")
        conv8 = net.getLayerId("conv8_313_rh")
        pts = pts.transpose().reshape(2, 313, 1, 1)
        net.getLayer(class8).blobs = [pts.astype("float32")]
        net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]
        print("Colorization model loaded successfully.")
    except Exception as e:
        print(f"Error loading colorization model: {e}")

def decode_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

def encode_image(image):
    _, buffer = cv2.imencode('.png', image)
    return base64.b64encode(buffer).decode('utf-8')

@app.post("/api/align")
async def align_images(historical: UploadFile = File(...), modern: UploadFile = File(...)):
    hist_bytes = await historical.read()
    mod_bytes = await modern.read()

    img_hist = decode_image(hist_bytes)
    img_mod = decode_image(mod_bytes)

    orb = cv2.ORB_create(5000)
    kp1, des1 = orb.detectAndCompute(img_hist, None)
    kp2, des2 = orb.detectAndCompute(img_mod, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)

    good_matches = matches[:50]
    points1 = np.zeros((len(good_matches), 2), dtype=np.float32)
    points2 = np.zeros((len(good_matches), 2), dtype=np.float32)

    for i, match in enumerate(good_matches):
        points1[i, :] = kp1[match.queryIdx].pt
        points2[i, :] = kp2[match.trainIdx].pt

    try:
        h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)
        if h is None:
            raise Exception("Homography could not be computed")
        height, width, _ = img_mod.shape
        img_aligned = cv2.warpPerspective(img_hist, h, (width, height))
        return {
            "historical": f"data:image/png;base64,{encode_image(img_aligned)}",
            "modern": f"data:image/png;base64,{encode_image(img_mod)}",
            "aligned": True
        }
    except Exception as e:
        return {
            "historical": f"data:image/png;base64,{encode_image(img_hist)}",
            "modern": f"data:image/png;base64,{encode_image(img_mod)}",
            "aligned": False,
            "error": str(e)
        }

@app.post("/api/colorize")
async def colorize_image(file: UploadFile = File(...)):
    if net is None:
        return {"error": "Colorization model not loaded"}
    contents = await file.read()
    image = decode_image(contents)
    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
    resized_l = cv2.resize(lab[:, :, 0], (224, 224))
    resized_l -= 50
    net.setInput(cv2.dnn.blobFromImage(resized_l))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))
    l = lab[:, :, 0]
    colorized = np.concatenate((l[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)
    colorized = (255 * colorized).astype("uint8")
    return {"image": f"data:image/png;base64,{encode_image(colorized)}"}

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
