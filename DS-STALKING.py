import os
import random
from flask import Flask, render_template, Response, request
import cv2
import threading

app = Flask(__name__)

# Choisir un port aléatoire
port = random.randint(1024, 65535)

# Variables pour le flux vidéo
camera_url = "http://<IP>/video_feed"  # Remplacez par l'URL de votre caméra
video_capture = cv2.VideoCapture(camera_url)

@app.route('/')
def home():
    return render_template("home.html", port=port)

@app.route('/start_stream')
def start_stream():
    return render_template("camera.html")

def gen_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)