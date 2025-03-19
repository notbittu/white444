from flask import Flask, request, jsonify
from flask_cors
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)
@app.route('/')
def home():
    return "Paint Home Backend is Running."

def calculate_shadow_effect(color, light_intensity):
    """Calculate how the color looks under different light intensities."""
    r, g, b = color
    factor = light_intensity / 100
    new_r = int(min(255, r * factor))
    new_g = int(min(255, g * factor))
    new_b = int(min(255, b * factor))
    return '#%02x%02x%02x' % (new_r, new_g, new_b)

@app.route('/color-suggestion', methods=['POST'])
def color_suggestion():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400

        image = request.files['image']
        img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"error": "Invalid image"}), 400

        # Calculate average color
        avg_color_per_row = np.average(img, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        avg_color = avg_color.astype(int)

        # Convert BGR to HEX
        hex_color = '#%02x%02x%02x' % (avg_color[2], avg_color[1], avg_color[0])

        # AI-based color suggestions (more realistic)
        suggestions = [
            hex_color,
            '#%02x%02x%02x' % ((avg_color[2] + 30) % 256, (avg_color[1] + 20) % 256, (avg_color[0] + 10) % 256),
            '#%02x%02x%02x' % ((avg_color[2] - 30) % 256, (avg_color[1] - 20) % 256, (avg_color[0] - 10) % 256),
        ]

        # Simulate different light intensities for shadow tracking
        shadow_effects = {
            "dim_light": calculate_shadow_effect(avg_color, 50),
            "normal_light": calculate_shadow_effect(avg_color, 100),
            "bright_light": calculate_shadow_effect(avg_color, 150)
        }

        response = {
            "average_color": hex_color,
            "suggestions": suggestions,
            "shadow_tracking": shadow_effects
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
