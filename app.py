from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

def calculate_shadow_effect(color, light_intensity):
    r, g, b = color
    factor = light_intensity / 100
    new_r = int(min(255, r * factor))
    new_g = int(min(255, g * factor))
    new_b = int(min(255, b * factor))
    return '#%02x%02x%02x' % (new_r, new_g, new_b)

@app.route('/color-suggestion', methods=['POST'])
def color_suggestion():
    try:
        image_file = request.files['image']
        if not image_file:
            return jsonify({'error': 'No file uploaded'}), 400

        image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        avg_color_per_row = np.average(image, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0).astype(int)
        avg_color = (avg_color[2], avg_color[1], avg_color[0])  # Convert BGR to RGB

        light_intensity = 80  # Example static value
        suggested_color = calculate_shadow_effect(avg_color, light_intensity)

        return jsonify({'suggested_color': suggested_color})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
