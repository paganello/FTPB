
import json
from src.utils import datetime_utils

# Reformat and input verifier
# Only "[date] [total]" or "[total]" are accepted

# Text format verifier
def text_slicer(text):
    list = text.split()

    # Se ci sono meno di 2 parole, aggiungi stringhe vuote per gli elementi mancanti
    if len(list) < 2:
        if float(list[0]):
            result = {
                "date": datetime_utils.get_formatted_datetime(),
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

    # Load the JSON objects
    j1 = json.loads(fields[0])
    j2 = json.loads(fields[1])

    # Check if the date is empty, if so, add the current datetime
    if j1["date"] == "" or j1["date"] == " ":
        j1["date"] = datetime_utils.get_formatted_datetime()

    # Separe the JSON objects put they in a list
    jFiles = [j1]
    for j2_file in j2:

        jFiles.append(j2_file)

    return jFiles


            
