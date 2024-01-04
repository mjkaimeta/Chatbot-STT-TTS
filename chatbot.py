from transformers import pipeline, Conversation
import pandas as pd
from datetime import datetime
import os


"""
NOTES:

The intention with this file is to outline a framework of how information can be passed from step to step of the chatbot + TTS/STT framework.
All of the 'pieces' should fit together, with each of the following components being interchangeable, as this is just a proof-of-concept

Conceptual components:
- Speech-to-Text module: records and transcribes user audio input
- LLM/chatbot: takes in user input (as text) and generates a meaningful response.
    Current implementation does not support context or RAG, though the intention is that piece of the framework CAN.
- Text-to-Speech: takes the LLM/chatbot's generated TEXT response and converts it to audio, which is then played aloud for the user
"""

# chatbot - this can be substituted for another model
pipe = pipeline("conversational", model = "facebook/blenderbot_small-90M")

def get_model_inference(user_text: str):
    """
    This function uses the Hugging Face's pipeline for conversational models to generate a response to the 
    provided user text. The model used is Facebook's Blenderbot.
    
    Parameters:
        user_text (str): The text input from the user to which the model will generate a response.
    
    Returns:
        str: The generated response from the model to the user's text. If an error occurs during the model inference, 
        it returns a string with the error message.
    
    Raises:
        Exception: If there's an error during the model inference.
    """
    convo = Conversation(user_text)

    # if there's model inference
    try:
        return pipe([convo])[-1]['content'] # str of most recent model message
    except Exception as e:
        return f"ERROR: {e}"
    
def get_current_datetime():
    """
    This function returns the current date and time as a string in the format 'YYYYMMDDHHMMSS'.
    
    Returns:
        str: The current date and time.
    """
    return datetime.now().strftime('%Y%m%d%H%M%S')

class Convo():
    """
    This class represents a conversation with a conversational model. It logs the turns of the conversation, 
    the user's and model's inputs, and optionally the inference times. It also provides methods to get the 
    conversation as a DataFrame and to create a log of the conversation.
    
    Attributes:
        history (list): A list of dictionaries representing the conversation log.
        model_name (str): The name of the conversational model.
        turn (int): The current turn of the conversation.
        inference_times (list): A list of dictionaries representing the inference times for each turn.
    """
    def __init__(self, model_name: str = None):
        """
        The constructor for the Convo class. Initializes the history, model_name, turn, and inference_times 
        attributes.

        Parameters:
            model_name (str): The name of the conversational model. Default is None.
        """
        self.history = [] # conversation log -> [{"turn": x, "user": "asdf", "model": "asdf"}, ...]
        self.model_name = "No model passed" if not model_name else model_name
        self.turn = 1
        self.inference_times = [] # [{"turn": int, "time": float_seconds}, ...] # optional
        self.convo_dir = ""

    def log_turn(self, user_content: str, model_content: str):
        """
        Logs a turn of the conversation, including the user's and model's inputs.
        Parameters:
        user_content (str): The user's input for this turn.
        model_content (str): The model's input for this turn.
        """
        self.history.append(
            {
                "turn": self.turn,
                "user" : user_content,
                "model" : model_content
            }
        )
        self.turn += 1 # increment turn

    def get_convo_df(self):
        """
        Converts the conversation log into a DataFrame.
        
        Returns:
            DataFrame: A DataFrame representing the conversation log.
        
        Raises:
            AssertionError: If there is not at least one full turn of conversation.
        """
        assert len(self.history) > 1, ("There must be at least one user turn and one model turn of conversation to create a DataFrame") # must be at least one full turn

        df_dict = {key: [] for key, _ in self.history[0].items()} # setup empty dict with same keys as history and lists
        for turn in self.history:
            for key, val in turn.items():
                df_dict[key].append(val)

        return pd.DataFrame(df_dict)

    def create_convo_log(self):
        """
        Creates a log of the conversation, saving it as both a .csv and .txt file in a folder named with the 
        current date and time.
        
        Raises:
            OSError: If the function is unable to create the folder or the files.
        """
        # create convo folder
        data_dir = "data/logged_convos/"
        datetime = get_current_datetime()
        convo_folder = f"{data_dir + datetime}"
        self.convo_dir = convo_folder

        if not os.path.exists(convo_folder):
            os.makedirs(convo_folder)
        
        base_file_name = f"{convo_folder}/{datetime}_convo"

        ### log convo in different formats
        # .csv
        convo_df = self.get_convo_df() #### CHANGE THIS
        convo_df.to_csv(f"{base_file_name}.csv", index = False) # 'turn' col functions as idx

        # .txt
        with open(f"{base_file_name}.txt", "w") as f:
            for turn_log in self.history:
                f.write(
                    f"Turn: {turn_log['turn']}\n\tUSER: {turn_log['user']}\n\tMODEL: {turn_log['model']}\n\n" # can be split by ("\n\n") later to get turn-by-turn
                    )