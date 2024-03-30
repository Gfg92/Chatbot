import threading
from gtts import gTTS
from io import BytesIO
import pygame

def play_audio(text):
        pygame.mixer.init()
        tts = gTTS(text, lang='en')
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        
        pygame.mixer.music.load(mp3_fp)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

def play_audio_thread(text):
    threading.Thread(target=play_audio, args=(text,)).start()
    
    