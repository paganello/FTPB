import json
from src.utils import datetime_utils


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
    if j1["date"] != "NULL":
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