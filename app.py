from flask import Flask, request, jsonify, send_file 
from flask_cors import CORS 
import os import cv2 
import numpy as np

app = Flask(__name__) 
CORS(app)

UPLOAD_FOLDER = "uploads" os.makedirs(UPLOAD_FOLDER, exist_ok=True)

Dummy AI suggestion

def suggest_colors(image_path): return ["#D32F2F", "#388E3C", "#1976D2"]

Realistic paint overlay using OpenCV

def apply_color_on_wall(image_path, hex_color): img = cv2.imread(image_path) img = cv2.resize(img, (500, 500))

hex_color = hex_color.lstrip('#')
bgr_color = tuple(int(hex_color[i:i+2], 16) for i in (4, 2, 0))

mask = cv2.inRange(img, (150, 150, 150), (255, 255, 255))
color_layer = np.full(img.shape, bgr_color, dtype=np.uint8)
colored_img = cv2.addWeighted(img, 0.6, color_layer, 0.4, 0)
img[mask > 0] = colored_img[mask > 0]

return img

@app.route('/') def home(): return jsonify({"message": "Paint Home Backend Live"})

@app.route('/upload', methods=['POST']) def upload_image(): file = request.files['image'] filename = os.path.join(UPLOAD_FOLDER, file.filename) file.save(filename)

ai_colors = suggest_colors(filename)
predefined_colors = ["#E91E63", "#2196F3", "#4CAF50", "#FF9800"]

return jsonify({
    "status": "success",
    "ai_colors": ai_colors,
    "predefined_colors": predefined_colors,
    "filename": file.filename
})

@app.route('/preview', methods=['POST']) def preview(): data = request.json image_path = os.path.join(UPLOAD_FOLDER, data['filename']) hex_color = data['color']

output = apply_color_on_wall(image_path, hex_color)
output_path = os.path.join(UPLOAD_FOLDER, "preview.jpg")
cv2.imwrite(output_path, output)

return send_file(output_path, mimetype='image/jpeg')

if __name__ == "__main__": app.run(debug=True)


