from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_talisman import Talisman
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
import time
import random
import imghdr
import logging

# --- Config ---
app = Flask(__name__)
CORS(app)
Talisman(app)

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
CLEANUP_THRESHOLD_SECS = 600  # 10 minutes

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.INFO)

# --- AI Color Palette ---
PALETTE = {
    "Argilla Earth": {"hex": "#D4A373", "rgb": (212, 163, 115)},
    "Ocean Breeze": {"hex": "#A8DADC", "rgb": (168, 218, 220)},
    "Lavender Mist": {"hex": "#CDB4DB", "rgb": (205, 180, 219)},
    "Mint Calm": {"hex": "#B7E4C7", "rgb": (183, 228, 199)}
}

# --- Helpers ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_image_safe(filepath):
    return imghdr.what(filepath) in ALLOWED_EXTENSIONS

def apply_color_overlay(image_path, color_rgb):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Failed to read image")
    overlay = np.full(image.shape, color_rgb[::-1], dtype=np.uint8)
    blended = cv2.addWeighted(image, 0.6, overlay, 0.4, 0)
    result_path = os.path.join(RESULT_FOLDER, os.path.basename(image_path))
    cv2.imwrite(result_path, blended)
    return result_path

def cleanup_old_files(folder, age_secs):
    now = time.time()
    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        if os.path.isfile(fpath) and (now - os.path.getmtime(fpath) > age_secs):
            try:
                os.remove(fpath)
                logging.info(f"Removed old file: {fpath}")
            except Exception as e:
                logging.error(f"Error removing file {fpath}: {e}")

# --- Routes ---
@app.route("/")
def index():
    return "✅ Paint Home Flask Backend is Running"

@app.route("/upload", methods=["POST"])
def upload_wall_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files['image']
    if not allowed_file(image_file.filename):
        return jsonify({"error": "Invalid file format"}), 400

    filename = secure_filename(image_file.filename)
    upload_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    image_file.save(upload_path)
    logging.info(f"Image saved to {upload_path}")

    if not is_image_safe(upload_path):
        os.remove(upload_path)
        return jsonify({"error": "Uploaded file is not a valid image"}), 400

    selected_color_name = random.choice(list(PALETTE.keys()))
    color_data = PALETTE[selected_color_name]
    try:
        result_path = apply_color_overlay(upload_path, color_data['rgb'])
    except Exception as e:
        return jsonify({"error": "Image processing failed", "details": str(e)}), 500

    cleanup_old_files(UPLOAD_FOLDER, CLEANUP_THRESHOLD_SECS)
    cleanup_old_files(RESULT_FOLDER, CLEANUP_THRESHOLD_SECS)

    return jsonify({
        "color_name": selected_color_name,
        "hex_code": color_data['hex'],
        "preview_url": f"/preview/{os.path.basename(result_path)}"
    })

@app.route("/preview/<filename>")
def serve_preview(filename):
    file_path = os.path.join(RESULT_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    return send_file(file_path, mimetype='image/jpeg')

# --- Start Server ---
if __name__ == "__main__":
    app.run(debug=True)
