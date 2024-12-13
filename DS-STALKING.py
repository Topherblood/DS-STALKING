from flask import Flask, render_template, request, jsonify
import socket
import random

app = Flask(__name__)

# Fonction pour obtenir l'IP locale
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

# La page d'accueil avec les images
@app.route("/")
def home():
    return render_template("home.html")

# Générer un lien de streaming lorsqu'un utilisateur clique sur une image
@app.route("/get_stream_link/<phone_id>", methods=["POST"])
def get_stream_link(phone_id):
    # Sélectionner un port aléatoire
    port = random.randint(1024, 65535)

    # Créer l'URL de streaming (remplacer par votre logique de streaming réelle)
    client_ip = get_local_ip()
    stream_url = f"http://{client_ip}:{port}/stream_{phone_id}"

    # Retourner le lien
    return jsonify({"stream_url": stream_url})

if __name__ == "__main__":
    # Exécuter le serveur Flask avec un port aléatoire
    port = random.randint(1024, 65535)
    local_ip = get_local_ip()
    print(f"Serveur en cours d'exécution sur : http://{local_ip}:{port}")
    app.run(host="0.0.0.0", port=port)