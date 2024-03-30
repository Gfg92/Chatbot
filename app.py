from flet import *
from controller.audio_controller import play_audio_thread
from controller.speech_recognition_controller import SpeechRecognition
from controller.ollama_controller import generate

def main(page: Page):

    def speech_recognition(e):
        recognized_text = SpeechRecognition.recognize_speech(e)
        txt_input.value = recognized_text
        on_input_change(e)
        page.update()
    def on_input_change(e):
        if len(txt_input.value) > 0:
            btn_mic.visible = False
            btn_send.visible = True
        else:
            btn_mic.visible = True
            btn_send.visible = False
        page.update()

    def send_message(e):

        if txt_input.value.strip():
            user_input = txt_input.value.strip()
        elif btn_mic.on_click:
            user_input = speech_recognition(e)

        if user_input:

            chat_view.controls.append(
                Container(
                    content= Column(
                        spacing=5,
                        controls=[
                                Row(
                                    spacing=5,
                                    controls=[
                                    CircleAvatar(
                                        content=Icon(icons.PERSON),
                                        scale=0.8,
                                        bgcolor= colors.BLUE
                                    ),
                                    Text(value="User")
                                ]),
                                Container(
                                    padding= padding.only(left=47),
                                    content= Text(value=f"{user_input}")
                                )
                            ]),
                    margin=margin.only(top= 10)
                )
                
            )
            txt_input.value = ""
            page.update()
            
            pre_response = Text(value="")
            chat_view.controls.append(
                Container(
                    content= Column(
                            spacing=5,
                            controls=[
                                Row(
                                    spacing=5,
                                    controls=[
                                    CircleAvatar(
                                        content=Text(value="B"),
                                        scale=0.8,
                                        bgcolor= colors.GREEN
                                    ),
                                    Text(value="Bot")
                                ]),
                                Container(
                                    padding= padding.only(left=47),
                                    content= pre_response
                                )
                            ]),
                    margin=margin.only(top= 10)
                )
            )
            page.update()
            
            response_text = ""
            for response_generate in generate(user_input):
                response_text += response_generate
                pre_response.value = response_text
                page.update()
            
            play_audio_thread(response_text)

    chat_view = ListView(expand= True, auto_scroll= True)
    btn_mic = IconButton(icon= icons.MIC, on_click=send_message)
    txt_input = TextField(hint_text="Type your message here", expand= True, autofocus= True, on_submit= send_message)
    btn_send = IconButton(icon= icons.SEND, on_click= send_message)
    input_row = Container(
            content= Row(
            [txt_input, btn_mic, btn_send], 
            alignment= alignment.bottom_center
            )
        )

    page.title = 'Chatbot'
    page.add(Column([chat_view, input_row], expand= True))

if __name__ == "__main__":
    app(target=main)