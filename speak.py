import os
from dotenv import load_dotenv
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, ResultReason
from azure.cognitiveservices.speech.audio import AudioOutputConfig

# Load environment variables
load_dotenv()

# Get Azure Speech Service credentials from environment variables
speech_key = os.getenv('AZURE_SPEECH_KEY')
speech_region = os.getenv('AZURE_SPEECH_REGION')

def text_to_speech(text):
    try:
        # Configure speech service
        speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
        
        # Set the voice to Portuguese (Brazil) - Male voice
        speech_config.speech_synthesis_voice_name = "pt-BR-LeticiaNeural"
        
        # Configure audio output (default speakers)
        audio_output = AudioOutputConfig(use_default_speaker=True)
        
        # Create synthesizer
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)
        
        # Synthesize text to speech
        result = synthesizer.speak_text_async(text).get()
        
        if result.reason == ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesis completed successfully")
        else:
            print(f"Speech synthesis failed: {result.reason}")
            
    except Exception as ex:
        print(f"Error occurred: {str(ex)}")

# Example usage
if __name__ == "__main__":
    phrase = "Bum bum tam tam"
    text_to_speech(phrase)
