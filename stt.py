import speech_recognition as sr # for STT
from tts import * # so this function can ask the user again for input if an error occurs
import time # checking how long it takes each step

def speech_to_text():
    """
    This function converts speech to text using Google's Speech Recognition API. It listens to the user's speech 
    through the microphone and returns the transcribed text. If the 'time_' parameter is set to True, the function 
    also measures and returns the time taken to transcribe the speech.
    
    Parameters:
        time_ (bool): If set to True, the function will return the time taken for speech recognition. Default is True.
    
    Returns:
        tuple: If 'time_' is True, a tuple containing the transcribed text in lower case and the time taken for 
        transcription is returned.
        str: If 'time_' is False, only the transcribed text in lower case is returned.
    
    Raises:
        sr.UnknownValueError: If the speech is not understood by the Google Speech Recognition API.
        sr.RequestError: If the function is unable to access the Google Speech Recognition API.
    """
    recognizer = sr.Recognizer()
    try_again_text = "Sorry, I couldn't understand. Please say that again."
    
    # Begin listening loop
    while True:
        with sr.Microphone() as source:
            # print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout = 10) # 10s timeout
        try:
            start = time.time()
            command = recognizer.recognize_google(audio)
            end = time.time() - start
            return command.lower(), end
        
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            text_to_speech(try_again_text)
            continue
        except sr.RequestError:
            print("Unable to access the Google Speech Recognition API.")
            text_to_speech(try_again_text)
            continue