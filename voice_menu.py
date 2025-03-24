import os
from dotenv import load_dotenv
from azure.cognitiveservices.speech import (
    SpeechConfig, 
    SpeechSynthesizer, 
    SpeechRecognizer,
    ResultReason,
)
from azure.cognitiveservices.speech.audio import AudioOutputConfig, AudioConfig

load_dotenv()
# Get Azure Speech Service credentials from environment variables
speech_key = os.getenv('AZURE_SPEECH_KEY')
speech_region = os.getenv('AZURE_SPEECH_REGION')

speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
speech_config.speech_synthesis_voice_name = "pt-BR-LeticiaNeural"
speech_config.speech_recognition_language = "pt-BR"
audio_output = AudioOutputConfig(use_default_speaker=True)
synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)
audio_config = AudioConfig(use_default_microphone=True)
recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

MENU_OPTIONS =  {
    "Saldo": "Você escolheu consultar o saldo da sua conta.",
    "Compra": "Você escolheu fazer uma simulação de compra internacional.",
    "Atendente": "Você escolheu falar com um atendente.",
    "Sair": "Obrigado por utilizar nossos serviços. Até logo!"
    }

def text_to_speech(text):
    try:
        synthesizer.speak_text_async(text).get()    
    except Exception as ex:
        print(f"TTS Error: {str(ex)}")

def speech_to_text():
    try:
        result = recognizer.recognize_once_async().get()
        if result.reason == ResultReason.RecognizedSpeech:
            print(f"Você disse: {result.text}")
            return result.text.lower()
        else:
            print("Não foi possível reconhecer o áudio")
            return None    
    except Exception as ex:
        print(f"STT Error: {str(ex)}")
        return None

def identify_option(text):
    if not text:
        return None
        
    text = text.lower()
    
    if "saldo" in text or "conta" in text or "1" in text or "um" in text:
        return "Saldo"
    elif "compra" in text or "internacional" in text or "2" in text or "dois" in text:
        return "Compra"
    elif "atendente" in text or "humano" in text or "3" in text or "três" in text:
        return "Atendente"
    elif "sair" in text or "encerrar" in text or "4" in text or "quatro" in text:
        return "Sair"
    
    return None

def play_menu():
    text_to_speech("""
    Bem-vindo ao atendimento automático da Quantm Finance.
    Por favor, escolha uma das seguintes opções: 
    1 - Consulta ao saldo da conta,
    2 - Simulação de compra internacional,
    3 - Falar com um atendente,
    4 - Sair do atendimento
""")

def main():
    play_menu()
    while True:
        user_input = speech_to_text()
        selected_option = identify_option(user_input)
        print(f"Você escolheu a opção {selected_option}")
        
        if selected_option:
            text_to_speech(MENU_OPTIONS[selected_option])
            if selected_option == "Sair":
                break
            else:
                play_menu()
        else:
            text_to_speech("Desculpe, não entendi sua opção. Escolha uma das opções disponíveis.")

if __name__ == "__main__":
    main() 