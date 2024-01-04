# Chatbot-STT-TTS
Proof-of-concept framework for integrating Speech-to-Text and Text-to-Speech with an existing LLM.

The LLM currently being used to generate responses is https://huggingface.co/facebook/blenderbot_small-90M. 

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

## Running Everything - main.py

You should now be able to use the model and have a conversation. Ensure you are in the right directory "Chatbot-STT-TTS/", and enter:

```
$ python main.py
```

NOTES:

1. The first time you run this, you will likely be prompted to download the LLM currently used in the framework. This is a relatively very small LLM, so the quality of the conversation will be poor compared to what we are used to.

2. Speak as cleary as you can. This may seem unnatural, but this Speech-to-Text module is not very high-quality, so it can easily produce innacurate results. Similar to the other pieces of this framework, the idea here is not that this will be the one used in production, but instead that this specific STT software can be replaced with something else conceptually equivalent as need be (and it currently definitely be).

3. Running this file should begin a conversation with the model in your CLI. Once began, the conversation will go indefinitely until one of the statements mentioned in the `break_conditions.txt` file are found in the transcription of a user's turn, at which point the model will conclude the conversation, and a conversation log will be created. Feel free to add more keywords/break conditions here or remove existing ones.

## Features & Future Work

RAG & Context
- Implement some sort of context across conversational turns. Current model does not have this in any capacity
- RAG is currently not implemented in any way in this chatbot, but with how things are laid out, it should be straightforward to create a RAG and/or contextually aware chatbot separate from this framework, so long as the LLM can take text input (user turn) and return text (model turn), which can then be easily added to this.

Conversation Summary
- Once a conversation is completed, create a summary of what was dicussed in the conversation. This is currently in-progress.

Logging/Functional
- Add log of inference time per turn for each STT, TTS, and model turn generation componenet (measuring these will make it easier to compare version improvements as these are modified)