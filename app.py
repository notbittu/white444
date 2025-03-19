from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import os

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
        # Extract image from the request
        image_file = request.files['image']
        image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Calculate average color of the wall
        avg_color_per_row = np.average(image, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        avg_color = avg_color.astype(int)
        avg_color = (avg_color[2], avg_color[1], avg_color[0])  # Convert BGR to RGB

        # Convert the average color to hex format
        hex_color = '#%02x%02x%02x' % avg_color

        # Color suggestions (You can add more colors here)
        suggestions = [
            '#ff6347',  # Tomato Red
            '#4682b4',  # Steel Blue
            '#32cd32',  # Lime Green
            '#ff8c00',  # Dark Orange
            '#8a2be2',  # Blue Violet
        ]

        # Shadow and light effects
        shadow_effects = {
            "dim_light": calculate_shadow_effect(avg_color, 50),
            "normal_light": calculate_shadow_effect(avg_color, 100),
            "bright_light": calculate_shadow_effect(avg_color, 150)
        }

        # Create response
        response = {
            "average_color": hex_color,
            "suggestions": suggestions,
            "shadow_tracking": shadow_effects
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
