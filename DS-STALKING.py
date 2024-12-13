from flask import Flask, render_template, request, jsonify
import socket
import random
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

# Fonction pour obtenir une IP locale
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
    # Cette fonction rend la page d'accueil avec des images de téléphone
    return render_template("home.html")

@app.route("/get_stream_link/<int:phone_id>", methods=["POST"])
def get_stream_link(phone_id):
    # Lorsqu'un utilisateur clique sur une image, on génère un lien de streaming
    client_ip = request.remote_addr
    random_port = random.randint(3000, 4000)  # Génère un port aléatoire pour le flux
    stream_url = f"http://{client_ip}:{random_port}/stream/{phone_id}"  # Lien de streaming unique
    return jsonify({"stream_url": stream_url})

if __name__ == "__main__":
    # Exécuter le serveur Flask
    local_ip = get_local_ip()
    print(f"Serveur en cours d'exécution sur : http://{local_ip}:5000")
    app.run(host="0.0.0.0", port=5000)  # Lancer le serveur Flask