import requests
from datetime import datetime

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
    