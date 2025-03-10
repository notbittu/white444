from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Paint Home Backend is Running!"

if __name__ == '__main__':

    if __name__=="__main__":
         app.run(host="0.0.0.0",
                 port=int(o.s.environ.get("PORT",5000)),
                 debug=True)
                 from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np

app = Flask(_name_)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    try:
        file = request.files['image']
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        
        # Dummy processing (You can replace with actual processing)
        processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        avg_color = int(np.mean(processed_img))

        return jsonify({'message': 'Scanning successful', 'average_color': avg_color})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
