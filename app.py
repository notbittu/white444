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
                 
