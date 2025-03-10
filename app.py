from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return "Paint Home Backend is Running."

@app.route('/color-suggestion', methods=['POST'])
def color_suggestion():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    image = request.files['image']
    img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"error": "Invalid image"}), 400

    # Get the average color of the image
    avg_color_per_row = np.average(img, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    avg_color = avg_color.astype(int)

    # Convert BGR to HEX color code
    hex_color = '#%02x%02x%02x' % (avg_color[2], avg_color[1], avg_color[0])

    # AI-based color suggestion (simple version)
    suggestions = [
        hex_color,
        '#%02x%02x%02x' % ((avg_color[2] + 50) % 256, (avg_color[1] + 30) % 256, (avg_color[0] + 10) % 256),
        '#%02x%02x%02x' % ((avg_color[2] - 50) % 256, (avg_color[1] - 30) % 256, (avg_color[0] - 10) % 256),
    ]

    return jsonify({"average_color": hex_color, "suggestions": suggestions})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
