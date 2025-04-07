from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

def apply_light_shadow_effect(rgb_color, intensity=80):
    """Simulate light/shadow by adjusting intensity."""
    factor = intensity / 100
    return '#{:02x}{:02x}{:02x}'.format(
        int(min(255, rgb_color[0] * factor)),
        int(min(255, rgb_color[1] * factor)),
        int(min(255, rgb_color[2] * factor))
    )

def get_dominant_color(image, k=4):
    """Find dominant color using KMeans (better than avg)."""
    pixels = image.reshape((-1, 3))
    pixels = np.float32(pixels)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, palette = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    dominant = palette[np.bincount(labels.flatten()).argmax()]
    return tuple(map(int, dominant[::-1]))  # BGR to RGB

@app.route('/color-suggestion', methods=['POST'])
def color_suggestion():
    try:
        file = request.files.get('image')
        if not file:
            return jsonify({'error': 'No image received'}), 400

        # Read and flip image (fix camera mirror)
        img_array = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        img = cv2.flip(img, 1)  # Flip horizontally

        dominant_rgb = get_dominant_color(img)
        suggested_color = apply_light_shadow_effect(dominant_rgb, intensity=85)

        return jsonify({
            'dominant_rgb': dominant_rgb,
            'suggested_color': suggested_color
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
