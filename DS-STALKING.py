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

# Fonction pour choisir un port aléatoire
def get_random_port():
    # Cette fonction renvoie un port aléatoire entre 3000 et 8000
    return random.randint(3000, 8000)

@app.route("/")
def home():
    # Retourne la page d'accueil lorsque l'utilisateur accède à /
    return render_template("home.html")

@app.route("/get_stream_link/<int:phone_id>", methods=["POST"])
def get_stream_link(phone_id):
    # Lorsqu'un utilisateur clique sur une image, un lien de streaming est généré
    client_ip = request.remote_addr
    random_port = get_random_port()  # Générer un port aléatoire
    stream_url = f"http://{client_ip}:{random_port}/stream/{phone_id}"  # Lien unique pour accéder au stream
    return jsonify({"stream_url": stream_url})

if __name__ == "__main__":
    # Récupère l'adresse IP locale du serveur
    local_ip = get_local_ip()
    
    # Génère un port aléatoire pour ce démarrage
    random_port = get_random_port()
    
    print(f"Serveur en cours d'exécution sur : http://{local_ip}:{random_port}")
    
    # Démarre le serveur Flask sur le port aléatoire
    app.run(host="0.0.0.0", port=random_port)