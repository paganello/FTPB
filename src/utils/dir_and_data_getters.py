import os
import json

from src.utils import datetime_utils 

# Path getter
def get_current_dir():
    """
    Returns the current directory path.

    Returns:
    - str: The current directory path.
    """
    return str(os.path.dirname(os.path.realpath(__file__)))


# Credential & Settings getters
def get_credentials(name):
    """
    Retrieves credentials from the credentials.json file.

    Args:
    - name (str): The name of the credential.

    Returns:
    - str or None: The value of the requested credential or None if not found.
    """
    file = open(get_current_dir() + '/../configs/credentials.json', 'r')
    cred = json.load(file)

    return str(cred[name])
    

# Settings getter
def get_settings(name):
    """
    Retrieves settings from the settings.json file.

    Args:
    - name (str): The name of the setting.

    Returns:
    - str or None: The value of the requested setting or None if not found.
    """
    file = open(get_current_dir() + '/../configs/settings.json', 'r')
    cred = json.load(file)
    
    return str(cred[name])
    

# Image name creator
def create_timebased_img_name():
    """
    Creates an image name based on the current datetime.

    Returns:
    - str: The image name.
    """
    return str(datetime_utils.get_current_datetime()) + ".jpg"
