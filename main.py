print("\nImporting packages...")

import pyperclip # for copying logged convo file path to clipboard lol
from chatbot import * # import chatbot + convo logging funcs
from stt import * # import STT funcs
from tts import * # import TTS funcs

BREAK_CONDS = [kw.lower().strip() for kw in open("break_conditions.txt", "r").readlines() if kw.strip()]

print("...packages imported. Beginning conversation.\n")
print("-------------\n")

def main(verbose: int = True, show_timing: bool = False):
    """
    This function initiates a conversation with the user, transcribes the user's speech to text, generates a 
    response using a conversational model, converts the response to speech, and logs the conversation. The 
    conversation continues until the user says a phrase that triggers a break condition. When the conversation 
    ends, the function logs the conversation and returns the conversation log.
    
    Parameters:
        show_timing (bool): If set to True, the function will print the time taken to listen to the user's input 
        and to generate the model's response. Default is False.
    
    Returns:
        Convo: An instance of the Convo class representing the conversation log.
        Raises:
        sr.UnknownValueError: If the speech is not understood by the Google Speech Recognition API.
        sr.RequestError: If the function is unable to access the Google Speech Recognition API.
        gTTSError: If the function is unable to access the Google Text-to-Speech API or if the text cannot be 
        processed into speech.
        PlaysoundException: If the function is unable to play the generated audio file.
        OSError: If the function is unable to delete the generated audio file or to create the conversation log.
        Exception: If there's an error during the model inference.
        """

    # opening message
    intro = "Hello. How can I be of assistance?"
    text_to_speech(intro)

    convo = Convo()

    while True:    

        if verbose:
            print("\n[[LISTENING]]\n\n") # to get overwritten by other text

        # Get voice input from user
        user_turn, listen_time = speech_to_text() # return time to listen

        # checks if break condition keywords are present in transcription
        break_now = any(brk_cnd.lower().strip() in user_turn.lower().strip() for brk_cnd in BREAK_CONDS)

        if verbose:    
            print(f'USER: "{user_turn}"')
            if show_timing:
                print(f"\t\n-- {round(listen_time, 2)}s to listen --\n\n") # rounded to 2 decimals

        # get model inference (no context, no RAG, etc., currently)
        inference_start = time.time()
        
        if break_now:
            # goodbye message to say to user
            model_turn = "Thank you. Have a nice day."
        else:
            model_turn = get_model_inference(user_turn)
        inference_end = time.time() - inference_start

        # play model's response aloud to the user
        text_to_speech(model_turn)
        
        if verbose:
            print(f'BOT: "{model_turn}"')
            if show_timing:
                print(f"\t\n-- {round(inference_end, 2)}s to get inference --\n") # rounded to 2 decimals
            else:
                print()

        convo.log_turn(
            user_content = user_turn,
            model_content = model_turn
            )

        # check if user is wanting to end the convo
        if break_now:

            # write convo log to drive
            convo.create_convo_log()
            pyperclip.copy(convo.convo_dir) # copy logged convo dir to user's clipboard to do something like "$ cd convo_path" or "$ open convo_path"
            
            if verbose:
                print(f"Conversation completed and written to drive at '{convo.convo_dir}'")
            
            break

# run it all
if __name__ == "__main__":
    main(verbose = False, show_timing = False) # can change to False if we don't want anything in the console