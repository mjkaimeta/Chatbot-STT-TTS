# Chatbot-STT-TTS
Proof-of-concept framework for integrating Speech-to-Text and Text-to-Speech with an existing LLM.

## Installation & Setup

1. To clone this repo, open your Command Line Interface (CLI) and enter the following. This will make a copy of the repository in your working directory, and then change your working directory to the downloaded repository folder.

```
$ git clone https://github.com/mjkaimeta/Chatbot-STT-TTS.git
$ cd Chatbot-STT-TTS
```

2. Next, you'll need to create a conda environment to ensure all necessary packages and dependencies are installed. To do this, ensure you first have anaconda installed and run the following in your CLI. Note that the conda environment name is currently "jarvis" (named after Iron Man's assistant), but you can change this, so long as you keep the name consistent anytime this name needs to be used at any point in this process.

```
$ conda env create -f environment.yaml
```

3. After successfully installing all dependencies, activate this conda environment with:

(Remember to change 'jarvis' to whatever name is listed in your environment.yaml file if you've changed it)

```
$ conda activate jarvis
```

4. You should now be able to use the model and have a conversation. Ensure you are in the right directory ("Chatbot-STT-TTS"), and run:

```
$ python main.py
```

## Running Everything - `main.py`

Running this file should begin a conversation with the model in your CLI. Once began, the conversation will go indefinitely until one of the statements mentioned in the "break_conditions.txt" file are found in the transcription of a user's turn, at which point the model will conclude the conversation, and a conversation log will be created. This is a turn-by-turn breakdown of the conversation. Currently, the log only has the transcription of the user's turns, and the model's turns.

## Future Work & Features

RAG & Context
- Implement some sort of context across conversational turns. Current model does not have this in any capacity
- RAG is currently not implemented in any way in this chatbot, but with how things are laid out, it should be straightforward to create a RAG and/or contextually aware chatbot separate from this framework, so long as the LLM can take text input (user turn) and return text (model turn), which can then be easily added to this

Conversation Summary
- Once a conversation is completed, create a summary of what was dicussed in the conversation