# import playsound # for playing the audio
import speech_recognition as sr # for STT
from tts import * # so this function can ask the user again for input if an error occurs
# from gtts import gTTS # for TTS (creates the audio file)
# from transformers import pipeline, Conversation
# import pandas as pd
# from datetime import datetime

# import os # to delete the audio file
import time # checking how long it takes each step
# from tqdm import tqdm

# # chatbot
# pipe = pipeline("conversational", model = "facebook/blenderbot_small-90M")

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

# def text_to_speech(response_text):
#     """
#     This function converts the provided text into speech using Google's Text-to-Speech (gTTS) API. It saves the 
#     generated speech as an mp3 file, plays the audio file, and then deletes the file.
    
#     Parameters:
#         response_text (str): The text to be converted into speech.
    
#     Note:
#         The function uses 'en' (English) as the language for the speech and 'co.za' as the Top Level Domain (TLD) 
#         to make the voice UK English.
    
#     Raises:
#         gTTSError: If the function is unable to access the Google Text-to-Speech API or if the text cannot be 
#         processed into speech.
#         PlaysoundException: If the function is unable to play the generated audio file.
#         OSError: If the function is unable to delete the generated audio file.
#     """
#     file_name = "response.mp3"
#     tts = gTTS(text=response_text, lang='en', tld='co.za') # made the voice UK English
#     tts.save(file_name)
#     playsound.playsound(file_name, True) 
#     os.remove(file_name) # delete the file after it's been created

# def get_model_inference(user_text: str):
#     """
#     This function uses the Hugging Face's pipeline for conversational models to generate a response to the 
#     provided user text. The model used is Facebook's Blenderbot.
    
#     Parameters:
#         user_text (str): The text input from the user to which the model will generate a response.
    
#     Returns:
#         str: The generated response from the model to the user's text. If an error occurs during the model inference, 
#         it returns a string with the error message.
    
#     Raises:
#         Exception: If there's an error during the model inference.
#     """
#     convo = Conversation(user_text)

#     # if there's model inference
#     try:
#         return pipe([convo])[-1]['content'] # str of most recent model message
#     except Exception as e:
#         return f"ERROR: {e}"
    
# def get_current_datetime():
#     """
#     This function returns the current date and time as a string in the format 'YYYYMMDDHHMMSS'.
    
#     Returns:
#         str: The current date and time.
#     """
#     return datetime.now().strftime('%Y%m%d%H%M%S')


# class Convo():
#     """
#     This class represents a conversation with a conversational model. It logs the turns of the conversation, 
#     the user's and model's inputs, and optionally the inference times. It also provides methods to get the 
#     conversation as a DataFrame and to create a log of the conversation.
    
#     Attributes:
#         history (list): A list of dictionaries representing the conversation log.
#         model_name (str): The name of the conversational model.
#         turn (int): The current turn of the conversation.
#         inference_times (list): A list of dictionaries representing the inference times for each turn.
#     """
#     def __init__(self, model_name: str = None):
#         """
#         The constructor for the Convo class. Initializes the history, model_name, turn, and inference_times 
#         attributes.

#         Parameters:
#             model_name (str): The name of the conversational model. Default is None.
#         """
#         self.history = [] # conversation log -> [{"turn": x, "user": "asdf", "model": "asdf"}, ...]
#         self.model_name = "No model passed" if not model_name else model_name
#         self.turn = 1
#         self.inference_times = [] # [{"turn": int, "time": float_seconds}, ...] # optional
#         self.convo_dir = ""

#     def log_turn(self, user_content: str, model_content: str):
#         """
#         Logs a turn of the conversation, including the user's and model's inputs.
#         Parameters:
#         user_content (str): The user's input for this turn.
#         model_content (str): The model's input for this turn.
#         """
#         self.history.append(
#             {
#                 "turn": self.turn,
#                 "user" : user_content,
#                 "model" : model_content
#             }
#         )
#         self.turn += 1 # increment turn

#     def get_convo_df(self):
#         """
#         Converts the conversation log into a DataFrame.
        
#         Returns:
#             DataFrame: A DataFrame representing the conversation log.
        
#         Raises:
#             AssertionError: If there is not at least one full turn of conversation.
#         """
#         assert len(self.history) > 1, ("There must be at least one user turn and one model turn of conversation to create a DataFrame") # must be at least one full turn

#         df_dict = {key: [] for key, _ in self.history[0].items()} # setup empty dict with same keys as history and lists
#         for turn in self.history:
#             for key, val in turn.items():
#                 df_dict[key].append(val)

#         return pd.DataFrame(df_dict)

#     def create_convo_log(self):
#         """
#         Creates a log of the conversation, saving it as both a .csv and .txt file in a folder named with the 
#         current date and time.
        
#         Raises:
#             OSError: If the function is unable to create the folder or the files.
#         """
#         # create convo folder
#         data_dir = "data/logged_convos/"
#         datetime = get_current_datetime()
#         convo_folder = f"{data_dir + datetime}"

#         if not os.path.exists(convo_folder):
#             os.makedirs(convo_folder)
        
#         base_file_name = f"{convo_folder}/{datetime}_convo"
#         self.convo_dir = base_file_name

#         ### log convo in different formats
#         # .csv
#         convo_df = self.get_convo_df() #### CHANGE THIS
#         convo_df.to_csv(f"{base_file_name}.csv", index = False) # 'turn' col functions as idx

#         # .txt
#         with open(f"{base_file_name}.txt", "w") as f:
#             for turn_log in self.history:
#                 f.write(
#                     f"Turn: {turn_log['turn']}\n\tUSER: {turn_log['user']}\n\tMODEL: {turn_log['model']}\n\n" # can be split by ("\n\n") later to get turn-by-turn
#                     )