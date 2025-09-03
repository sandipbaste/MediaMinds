from gtts import gTTS
import os

def text_to_speech(text: str, file_id: str) -> str:
    """
    Convert text to speech using gTTS
    """
    try:
        # Limit text length for TTS
        if len(text) > 4000:
            text = text[:4000] + "... (content truncated for audio)"
        
        tts = gTTS(text=text, lang='en', slow=False)
        audio_path = f"static/audio/{file_id}.mp3"
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        tts.save(audio_path)
        return audio_path
    
    except Exception as e:
        raise Exception(f"Error generating audio: {str(e)}")