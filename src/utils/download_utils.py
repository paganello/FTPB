import requests

def download_file(url, file_path):
    """
    Downloads a file from the specified URL and saves it to the specified file path.

    Args:
    - url (str): The URL of the file to download.
    - file_path (str): The file path where the downloaded file will be saved.

    Returns:
    - bool: True if the file is downloaded successfully, False otherwise.
    """
    # Execute the HTTP request to download the file
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)

        return True
    else:
        return False
