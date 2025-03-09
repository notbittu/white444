from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Paint Home Backend is Running!"

if __name__ == '__main__':
    app.run(debug=True)