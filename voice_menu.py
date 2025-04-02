import os
from dotenv import load_dotenv
from azure.cognitiveservices.speech import (
    SpeechConfig, 
    SpeechSynthesizer, 
    SpeechRecognizer,
    ResultReason,
    CancellationReason
)
from azure.cognitiveservices.speech.audio import AudioOutputConfig, AudioConfig

# Load environment variables
load_dotenv()

# Get Azure Speech Service credentials from environment variables
speech_key = os.getenv('AZURE_SPEECH_KEY')
speech_region = os.getenv('AZURE_SPEECH_REGION')

# Create audio directory if it doesn't exist
AUDIO_DIR = "audio_files"
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

MENU_OPTIONS = {
    "1": {
        "response": "Você escolheu consultar o saldo da sua conta.",
        "response_audio": "saldo_response.wav",
        "keywords": ["saldo", "conta", "1", "um", "primeiro", "primeira"]
    },
    "2": {
        "response": "Você escolheu fazer uma simulação de compra internacional.",
        "response_audio": "compra_response.wav",
        "keywords": ["compra", "internacional", "2", "dois", "segundo", "segunda"]
    },
    "3": {
        "response": "Você escolheu falar com um atendente.",
        "response_audio": "atendente_response.wav",
        "keywords": ["atendente", "humano", "3", "três", "terceiro", "terceira"]
    },
    "4": {
        "response": "Obrigado por utilizar nossos serviços. Até logo!",
        "response_audio": "sair_response.wav",
        "keywords": ["sair", "encerrar", "4", "quatro", "quarto", "quarta"]
    }
}

# Fixed audio files for system messages
SYSTEM_MESSAGES = {
    "welcome": {
        "text": "Bem-vindo ao atendimento automático da Quantm Finance.",
        "audio_file": "welcome.wav"
    },
    "menu": {
        "text": "Por favor, escolha uma das seguintes opções. Opção 1: Consulta ao saldo da conta. Opção 2: Simulação de compra internacional. Opção 3: Falar com um atendente. Opção 4: Sair do atendimento.",
        "audio_file": "menu.wav"
    },
    "error": {
        "text": "Desculpe, não entendi sua opção.",
        "audio_file": "error.wav"
    }
}

def get_audio_path(filename):
    return os.path.join(AUDIO_DIR, filename)

def text_to_speech(text, audio_file):
    try:
        audio_path = get_audio_path(audio_file)
        
        # If audio file already exists, play it
        if os.path.exists(audio_path):
            print(f"Using cached audio for: {text}")
            play_audio_file(audio_path)
            return

        # Configure speech service
        speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
        speech_config.speech_synthesis_voice_name = "pt-BR-LeticiaNeural"
        
        # Configure audio output to save to file
        audio_output = AudioOutputConfig(filename=audio_path)
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)
        
        # Synthesize text to speech
        result = synthesizer.speak_text_async(text).get()
        
        if result.reason == ResultReason.SynthesizingAudioCompleted:
            print(f"TTS: {text}")
            # Play the newly created audio file
            play_audio_file(audio_path)
        else:
            print(f"TTS failed: {result.reason}")
            
    except Exception as ex:
        print(f"TTS Error: {str(ex)}")

def play_audio_file(filename):
    try:
        if os.name == 'nt':  # Windows
            os.system(f'start wmplayer "{filename}"')
        elif os.name == 'posix':  # macOS and Linux
            os.system(f'afplay "{filename}"')
    except Exception as ex:
        print(f"Error playing audio file: {str(ex)}")

def speech_to_text():
    """Convert speech to text using Azure STT"""
    try:
        speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
        speech_config.speech_recognition_language = "pt-BR"
        audio_config = AudioConfig(use_default_microphone=True)
        recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        
        print("Escutando...")
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
    
    # Check for keywords in the text
    for option_id, option in MENU_OPTIONS.items():
        for keyword in option["keywords"]:
            if keyword in text:
                return option_id
    
    return None

def play_menu():
    text_to_speech(SYSTEM_MESSAGES["menu"]["text"], SYSTEM_MESSAGES["menu"]["audio_file"])

def main():
    # Play welcome message
    text_to_speech(SYSTEM_MESSAGES["welcome"]["text"], SYSTEM_MESSAGES["welcome"]["audio_file"])

    while True:
        play_menu()
        
        # Get user input through speech
        user_input = speech_to_text()
        
        # Identify the selected option
        selected_option = identify_option(user_input)
        
        if selected_option:
            # Play the corresponding response
            text_to_speech(MENU_OPTIONS[selected_option]["response"], 
                         MENU_OPTIONS[selected_option]["response_audio"])
            
            # If option 4 (exit) was selected, break the loop
            if selected_option == "4":
                break
        else:
            # If no option was identified, play error message and continue
            text_to_speech(SYSTEM_MESSAGES["error"]["text"], 
                         SYSTEM_MESSAGES["error"]["audio_file"])

if __name__ == "__main__":
    main() 