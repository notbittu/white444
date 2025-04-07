from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename

# Config
app = Flask(_name_)
CORS(app)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Utils
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def apply_ai_color(image):
    """
    Simulates AI-based color suggestion by enhancing warmth.
    In future, replace this with actual ML model logic.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = cv2.add(s, 25)
    v = cv2.add(v, 10)
    enhanced = cv2.merge((h, s, v))
    result = cv2.cvtColor(enhanced, cv2.COLOR_HSV2BGR)
    return result


# Routes
@app.route('/')
def index():
    return jsonify({'status': 'Paint Home Backend Active', 'version': '1.0.0'})


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Empty file name'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(RESULT_FOLDER, 'colored_' + filename)

    file.save(input_path)

    image = cv2.imread(input_path)
    if image is None:
        return jsonify({'error': 'Failed to process image'}), 500

    processed = apply_ai_color(image)
    cv2.imwrite(output_path, processed)

    return send_file(output_path, mimetype='image/jpeg')


# Start
if _name_ == '_main_':
    app.run(host='0.0.0.0', port=10000)
