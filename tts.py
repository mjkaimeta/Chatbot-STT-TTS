import os
import playsound # for playing the audio
from gtts import gTTS # for TTS (creates the audio file)

def text_to_speech(response_text):
    """
    This function converts the provided text into speech using Google's Text-to-Speech (gTTS) API. It saves the 
    generated speech as an mp3 file, plays the audio file, and then deletes the file.
    
    Parameters:
        response_text (str): The text to be converted into speech.
    
    Note:
        The function uses 'en' (English) as the language for the speech and 'co.za' as the Top Level Domain (TLD) 
        to make the voice UK English.
    
    Raises:
        gTTSError: If the function is unable to access the Google Text-to-Speech API or if the text cannot be 
        processed into speech.
        PlaysoundException: If the function is unable to play the generated audio file.
        OSError: If the function is unable to delete the generated audio file.
    """
    file_name = "response.mp3"
    tts = gTTS(text=response_text, lang='en', tld='co.za') # UK English voice
    tts.save(file_name) # saves generated speech file based on `response_text`
    playsound.playsound(file_name, True) 
    os.remove(file_name) # delete the file after it's been created