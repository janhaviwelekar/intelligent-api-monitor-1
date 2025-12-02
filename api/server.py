from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

@app.route('/ping')
def ping():
    return jsonify({"status": "ok", "message": "Fast response"})

@app.route('/slow')
def slow():
    delay = random.uniform(1, 3)
    time.sleep(delay)
    return jsonify({"status": "ok", "delay": delay})

@app.route('/error')
def error():
    if random.random() < 0.4:
        return jsonify({"status": "error", "message": "Random failure"}), 500
    return jsonify({"status": "ok", "message": "Sometimes error"})
    
if __name__ == "__main__":
    app.run(port=5001, debug=True)
