import json
from src.utils import datetime_utils

# Reformat and input verifier
# Only "[date] [total]" or "[total]" are accepted

# Text format verifier
def text_slicer(text):
    """
    Slices the input text into date and total, returns a dictionary.

    Args:
    - text (str): The input text.

    Returns:
    - dict: A dictionary containing date and total.
    """
    list = text.split()

    # If there are less than 2 words, add empty strings for the missing elements
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
    """
    Verifies the format of the input JSON.

    Args:
    - input_json (dict): The input JSON object.

    Returns:
    - bool: True if the format is correct, False otherwise.
    """
    # Check if the first element is a string
    if not isinstance(input_json["date"], str):
        print("date is not a string")
        return False
    
    # Check if the second element is float or int
    elif not isinstance(input_json["total"], float) and not isinstance(input_json["total"], int):
        print("total is not a float or int")
        return False
    
    else:
        return True
    

def json_reformatter(payload):
    """
    Reformat and load the JSON objects from the payload string.

    Args:
    - payload (str): The input payload string.

    Returns:
    - list: A list containing the reformatted JSON objects.
    """
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
    j3 = json.loads(fields[2])

    # Check if the date is empty, if so, add the current datetime
    # If the date is in the wrong format, replace the '/' with '-'
    if j1["date"] != "" or j1["date"] != "NULL":
        if "/" in j1["date"]:
            j1["date"] = replace_slash_with_dash(j1["date"])

    else:
        j1["date"] = datetime_utils.get_formatted_datetime()

    # Separate the JSON objects and put them in a list
    jFiles = [j1, j2]
    for j3_file in j3:

        jFiles.append(j3_file)

    return jFiles


def replace_slash_with_dash(input_string):
    """
    Replaces '/' characters with '-' in the input string.

    Args:
    - input_string (str): The input string.

    Returns:
    - str: The string with '/' characters replaced by '-'.
    """
    return input_string.replace("/", "-")