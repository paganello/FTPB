import os
import json
import requests
from datetime import datetime

# Path getter
def get_current_dir():
    return os.path.dirname(os.path.realpath(__file__))


# Credential & Settings getters
def get_credentials(name):

    file = open(get_current_dir() + '/configs/credentials.json', 'r')
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
    file = open(get_current_dir() + '/configs/settings.json', 'r')
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
    

# Reformat and input verifier
# Only "[date] [total]" or "[total]" are accepted

# Text format verifier
def text_slicer(text):
    list = text.split()

    # Se ci sono meno di 2 parole, aggiungi stringhe vuote per gli elementi mancanti
    if len(list) < 2:
        if float(list[0]):
            result = {
                "date": get_formatted_datetime(),
                "total": list[0]
            }
    else:
        result = {
            "date": list[0],
            "total": list[1]
        }

    print(result)
    print("text_slicer executed")
    return result

def verify_formatted_text_input(input_json):

    # Verifica se il primo elemento è una stringa
    if not isinstance(input_json["date"], str):
        print("date is not a string")
        return False
    
    # Verifica se il secondo elemento è float
    elif not isinstance(input_json["total"], float) or not isinstance(input_json["total"], int):
        print("total is not a float or int")
        return False
    
    else:
        return True
    
def json_reformatter(payload):

    # Remove all the unwanted characters
    fields = payload.strip()
    fields = payload.strip("'")
    fields = fields.strip('\n')
    fields = fields.strip('\n\n')

    # Split the string into two parts
    fields = payload.split(';')

    print (fields) #debug

    # Load the JSON objects
    j1 = json.loads(fields[0])
    j2 = json.loads(fields[1])

    print(j1)
    print("-----")
    print(j2)

    # Check if the date is empty, if so, add the current datetime
    if j1["date"] == "" or j1["date"] == " ":
        j1["date"] = get_formatted_datetime()

    # Separe the JSON objects put they in a list
    jFiles = [j1]
    for j2_file in j2:

        jFiles.append(j2_file)


    print(jFiles[1]["amount"])
    return jFiles

# Current time getter
def get_current_datetime():
    try:
        # execute HTTP request to get the current time
        response = requests.get("http://worldtimeapi.org/api/ip")
        data = response.json()
        datetime_str = data['datetime']

        # Remove milliseconds from the datetime string
        return datetime_str.split('.')[0] 
    
    except requests.RequestException as e:

        print("Errore durante la richiesta HTTP:", e)
        return None

def format_datetime(datetime_str):
    try:

        # Analizza la stringa di data e ora in un oggetto datetime
        dt_obj = datetime.fromisoformat(datetime_str)

        # Formatta l'oggetto datetime nel formato desiderato
        formatted_datetime = dt_obj.strftime('%Y-%m-%d %H:%M')
        return formatted_datetime
    
    except ValueError as e:
        return None
    
def get_formatted_datetime():

    # Ottieni la data e l'ora correnti
    current_datetime = get_current_datetime()

    # Formatta la data e l'ora correnti
    if current_datetime:
        return format_datetime(current_datetime)
    else:
        return None
    

def download_file(url, file_path):
    
    # Execute the HTTP request to download the file
    r = requests.get(url, stream=True)

    with open(file_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)

    return True

            
