import pycurl, json
from io import BytesIO
from datetime import datetime

# Current time getter
def get_current_datetime():
    """
    Retrieves the current datetime from the worldtimeapi.org.

    Returns:
    - str or None: The current datetime string or None if an error occurs.
    """
    # Execute HTTP cURL request to get the current time (request.get can be block by worldtimeapi.org)
    url = 'http://worldtimeapi.org/api/ip'
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()

    # Body is a byte string.
    # We have to know the encoding in order to print it to a text file
    # such as standard output.
    date = json.loads(body.decode('iso-8859-1'))
    datetime_str = date['datetime']

    # Remove milliseconds from the datetime string
    return datetime_str.split('.')[0] 



def format_datetime(datetime_str):
    """
    Formats the input datetime string into the desired format.

    Args:
    - datetime_str (str): The input datetime string.

    Returns:
    - str or None: The formatted datetime string or None if the input is invalid.
    """
    try:
        # Parse the datetime string into a datetime object
        dt_obj = datetime.fromisoformat(datetime_str)

        # Format the datetime object into the desired format
        formatted_datetime = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_datetime
    
    except ValueError as e:
        return None
    

def get_formatted_datetime():
    """
    Retrieves the current datetime and formats it into the desired format.

    Returns:
    - str or None: The formatted current datetime string or None if an error occurs.
    """
    # Get the current date and time
    current_datetime = get_current_datetime()

    # Format the current date and time
    if current_datetime:
        return format_datetime(current_datetime)
    else:
        return None
