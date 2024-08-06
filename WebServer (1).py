import threading
from flask import Flask

app = Flask(__name__)

@app.route("/")
def ping():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

def keep_alive():
    t = threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8080, debug=False))
    t.start() 
