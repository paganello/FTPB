import requests

def download_file(url, file_path):
    
    # Execute the HTTP request to download the file
    r = requests.get(url, stream=True)

    with open(file_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)

    return True