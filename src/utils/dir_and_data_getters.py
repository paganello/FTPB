import os
import json

# Path getter
def get_current_dir():
    return os.path.dirname(os.path.realpath(__file__))


# Credential & Settings getters
def get_credentials(name):

    file = open(get_current_dir() + '/../configs/credentials.json', 'r')
    cred = json.load(file)

    if name == "TELEGRAM_TOKEN":
        TELEGRAM_TOKEN = cred["TELEGRAM_TOKEN"]
        return TELEGRAM_TOKEN
    
    elif name == "AZURE_API_KEY":
        AZURE_API_KEY = cred["AZURE_API_KEY"]
        return AZURE_API_KEY
    
    elif name == "AZURE_ENDPOINT":
        AZURE_ENDPOINT = cred["AZURE_ENDPOINT"]
        return AZURE_ENDPOINT
    
    elif name == "OPENAI_API_KEY":
        OPENAI_API_KEY = cred["OPENAI_API_KEY"]
        return OPENAI_API_KEY
    
    else:
        return None
    

def get_settings(name):
    file = open(get_current_dir() + '/../configs/settings.json', 'r')
    cred = json.load(file)
    
    if name == "IMAGE_NAME":
        IMAGE_NAME = cred["IMAGE_NAME"]
        return IMAGE_NAME
    
    elif name == "ASSISTANT_INSTRUCTIONS":
        ASSISTANT_INSTRUCTIONS = cred["ASSISTANT_INSTRUCTIONS"]
        return ASSISTANT_INSTRUCTIONS
    
    elif name == "CUSTOM_MODEL_NAME":
        CUSTOM_MODEL_NAME = cred["CUSTOM_MODEL_NAME"]
        return CUSTOM_MODEL_NAME
    
    elif name == "CUSTOM_MODEL_SYS_INSTRUCTIONS":
        CUSTOM_MODEL_SYS_INSTRUCTIONS = cred["CUSTOM_MODEL_SYS_INSTRUCTIONS"]
        return CUSTOM_MODEL_SYS_INSTRUCTIONS

    else:
        return None
    