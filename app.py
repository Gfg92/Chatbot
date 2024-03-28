import flet as ft
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
import pygame
import tempfile
import threading

def main(page: ft.Page):
    pygame.mixer.init()
    page.title = "Developer Chatbot"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def btn_click(e):
        if not txt_input.value:
            txt_input.error_text = "Por favor, ingresa un mensaje"
            page.update()
        else:
            txt_input.error_text = None
            user_message = ft.Container(
                content=ft.Row(
                    [
                        ft.CircleAvatar(
                            foreground_image_url="https://www.example.com/user_avatar.png",
                            content=ft.Text("U"),
                        ),
                        ft.Column(
                            [
                                ft.Text(f"{txt_input.value}", color=ft.colors.BLACK),
                            ],
                            spacing=5,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
                padding=ft.padding.all(10),
                border_radius=ft.border_radius.all(10),
                bgcolor=ft.colors.BLUE_GREY_100,
            )
            chat_view.controls.append(user_message)

            chatbot_response = get_chatbot_response(txt_input.value)
            bot_message = ft.Container(
                content=ft.Row(
                    [
                        ft.CircleAvatar(
                            foreground_image_url="https://www.example.com/bot_avatar.png",
                            content=ft.Text("B"),
                        ),
                        ft.Column(
                            [
                                ft.Text(f"{chatbot_response}", color=ft.colors.BLACK),
                            ],
                            spacing=5,
                        ),
                    ],
                ),
                padding=ft.padding.all(10),
                border_radius=ft.border_radius.all(10),
                bgcolor=ft.colors.BLUE_GREY_200,
            )
            chat_view.controls.append(bot_message)

            txt_input.value = ""
            btn_mic.visible = True 
            btn_send.visible = False  
            page.update()

    def play_audio_thread(text):
        threading.Thread(target=play_audio, args=(text,)).start()

    # def get_chatbot_response(user_input):
    #     response = "Hola, ¿Cómo te llamas?"
    #     play_audio_thread(response)
    #     return response
        
    def get_chatbot_response(user_input):
        llm = Ollama(model="mistral")

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are the best spanish software developer. You response in spanish languaje."),
            ("user", user_input)
        ])
        prompt_string = prompt.format_prompt()
        response = llm.invoke(prompt_string)
        play_audio_thread(response)
        return response

    def recognize_speech(e):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Habla ahora...")
            audio = r.listen(source)
            print("Ha dejado de escuchar!")

        try:
            text = r.recognize_whisper(audio, language="es")
            txt_input.value = text
            on_input_change(None)
            page.update()
        except sr.UnknownValueError:
            print("No se pudo reconocer el audio")
        except sr.RequestError as e:
            print(f"Error al solicitar el servicio de reconocimiento de voz; {e}")

    def play_audio(text):
        tts = gTTS(text, lang='es')
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        
        pygame.mixer.music.load(mp3_fp)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def on_input_change(e):
        if len(txt_input.value) > 0:
            btn_mic.visible = False
            btn_send.visible = True
        else:
            btn_mic.visible = True
            btn_send.visible = False
        page.update()

    txt_input = ft.TextField(
        hint_text="Escribe tu mensaje...",
        expand=True,
        on_submit=btn_click,
        on_change=on_input_change,
    )

    btn_mic = ft.IconButton(
        icon=ft.icons.MIC,
        tooltip="Grabar mensaje de voz",
        on_click=recognize_speech,
    )

    btn_send = ft.ElevatedButton(
        "Enviar",
        on_click=btn_click,
        visible=False,
    )

    chat_view = ft.ListView(expand=True, spacing=10, auto_scroll=True)

    page.add(
        chat_view,
        ft.Row(
            [
                txt_input,
                ft.Stack(
                    [
                        btn_mic,
                        btn_send,
                    ],
                ),
            ],
        )
    )

ft.app(target=main)