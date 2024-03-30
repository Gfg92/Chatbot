import speech_recognition as sr

class SpeechRecognition:
    def __init__(self, model):
        self.model = model
    
    def recognize_speech(e):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Habla ahora...")
            audio = r.listen(source)
            print("Ha dejado de escuchar!")
        try:
            text = r.recognize_whisper(audio, language="es")
            print(text)
            return text
        except sr.UnknownValueError:
            print("No se pudo reconocer el audio")
        except sr.RequestError as e:
            print(f"Error al solicitar el servicio de reconocimiento de voz; {e}")