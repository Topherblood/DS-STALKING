from flask import Flask, render_template, request, jsonify, url_for
import socket

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
    # Page qui demande l'accès à la caméra et au micro
    return render_template("camera.html")

@app.route("/stream_link", methods=["POST"])
def stream_link():
    # Génère un lien contenant l'adresse IP et le port
    client_ip = request.remote_addr
    port = 5000  # Remplacez si nécessaire
    stream_url = f"http://{client_ip}:{port}/stream"
    return jsonify({"stream_url": stream_url})

if __name__ == "__main__":
    # Exécute le serveur Flask
    local_ip = get_local_ip()
    print(f"Serveur en cours d'exécution : http://{local_ip}:5000")
    app.run(host="0.0.0.0", port=5000)
