import mysql.connector
from src.utils import dir_and_data_getters

class DataBaseHandler:
    
    def __init__(self, db_addr, db_user, db_psw, db_name):
        """
        Initializes the database handler with connection parameters.
        
        Args:
        - db_psw (str): Password for the database.
        - db_addr (str): Address of the database server.
        - db_user (str): Username for accessing the database.
        - db_name (str): Name of the database.
        """
        self.db_psw = db_psw
        self.db_user = db_user
        self.db_addr = db_addr
        self.db_name = db_name
        self.connection = None
    
    
    def connect(self):
        """
        Connects to the database using the provided connection parameters.
        
        Returns:
        - bool: True if connection is successful, False otherwise.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.db_addr,
                user=self.db_user,
                password=self.db_psw,
                database=self.db_name
            )
            return True

        except mysql.connector.Error as err:
            return False
    
    
    def disconnect(self):
        """
        Disconnects from the database.
        """
        if self.connection:
            self.connection.close()

    
    def execute_querys(self, querys):
        """
        Executes a list of SQL queries.
        
        Args:
        - querys (list): List of SQL queries to be executed.
        
        Returns:
        - bool: True if all queries are executed successfully, False otherwise.
        """
        try: 
            cursor = self.connection.cursor()

        except mysql.connector.Error as err:
            return False

        for query in querys:

            #try: 
                cursor.execute(query)

            #except mysql.connector.Error as err:
            #    cursor.close()
            #    return False

        try: 
            self.connection.commit()
            cursor.close()

            return True
        
        except mysql.connector.Error as err:
            cursor.close()
            return False
        
    
    def fetch(self, query):
        """
        Fetches data from the database based on the provided SQL query.
        
        Args:
        - query (str): SQL query to fetch data.
        
        Returns:
        - list: List of tuples containing the fetched data, or None if an error occurs.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        
        except mysql.connector.Error as err:
            return None

        finally:
            cursor.close()




def update(jsons, img_name=None):
    """
    Updates the database with the provided JSON data.
    
    Args:
    - jsons (list): List of JSON objects containing transaction information.
    - img_name (str): Name of the image file associated with the transactions, if any.
    
    Returns:
    - bool: True if update is successful, False otherwise.
    """
    db_addr = dir_and_data_getters.get_credentials('DB_ADDRESS')
    db_user = dir_and_data_getters.get_credentials('DB_USER')
    db_psw = dir_and_data_getters.get_credentials('DB_PWD')
    db_name = dir_and_data_getters.get_credentials('DB_NAME')

    db = DataBaseHandler(db_addr, db_user, db_psw, db_name)

    db.connect()

    transaction_query = create_query_array(jsons, img_name)
    
    if db.execute_querys(transaction_query):

        jsons.pop(0)
        querys = create_query_array(jsons)

        if db.execute_querys(querys):
            db.disconnect()
            return True
    
        else:
            db.disconnect()
            return False
        
    else:
        db.disconnect()
        return False
    


def create_query_array(jsons, img_name=None):
    """
    Creates a list of SQL queries based on the provided JSON data.

    Args:
    - jsons (list): List of JSON objects containing transaction information.
    - img_name (str): Name of the image file associated with the transactions, if any.

    Returns:
    - list: List of SQL queries.
    """

    # Initialize an empty list to store SQL queries
    querys = []
    transaction_ID = None

    # Iterate over each JSON object in the list
    for json_file in jsons:

        # Check if the JSON object contains transaction information
        if "date" in json_file and "total" in json_file and "receipt_ID" in json_file:

            # Process the values and format them for SQL insertion
            if img_name is None:
                receipt_file_name = "NULL"
            else:
                receipt_file_name = "'{}'".format(img_name)

            date = process_value(json_file.get("date", "NULL"))
            total = process_value(json_file.get("total", "NULL"))
            receipt_ID = process_value(json_file.get("receipt_ID", "NULL"))

            # Truncate the values to fit the database constraints
            date = date[:16+2]
            receipt_ID = receipt_ID[:9+2]
            receipt_file_name = receipt_file_name[:23+2]

            # Construct the SQL query and append it to the list
            querys.append("INSERT INTO transaction (date, total, receipt_ID, receipt_file_name) VALUES ({}, {}, {}, {});".format(date, total, receipt_ID, receipt_file_name)) 

            # Return the list of queries (exit loop after the first transaction)
            return querys
        
        # Check if the JSON object contains information about goods
        if "amount" in json_file and "tax" in json_file and "description" in json_file:
            if transaction_ID is None:
                transaction_ID = get_last_id()

            amount = process_value(json_file.get("amount", "NULL"))
            tax = process_value(json_file.get("tax", "NULL"))
            description = process_value(json_file.get("description", "NULL"))

            # Truncate the description to fit the database constraints
            description = description[:64+2]

            # Construct the SQL query and append it to the list
            querys.append("INSERT INTO good (transaction_ID, amount, tax, description) VALUES ('{}', {}, {}, {});".format(transaction_ID,  amount, tax, description))

        # Check if the JSON object contains information about stores
        if "name" in json_file and "address" in json_file and "city" in json_file and "VAT" in json_file:
            if transaction_ID is None:
                transaction_ID = get_last_id()

            name = process_value(json_file.get("name", "NULL"))
            address = process_value(json_file.get("address", "NULL"))
            city = process_value(json_file.get("city", "NULL"))
            VAT = process_value(json_file.get("VAT", "NULL"))

            # Truncate the values to fit the database constraints
            name = name[:64+2]
            address = address[:64+2]
            city = city[:64+2]
            VAT = VAT[:16+2]

            # Construct the SQL query and append it to the list
            querys.append("INSERT INTO store (transaction_ID, name, address, city, VAT) VALUES ('{}', {}, {}, {}, {});".format(transaction_ID, name, address, city, VAT))

    return querys

def process_value(value):
    """
    Used only in the create_query_array function.
    Processes the input value for SQL insertion.

    Args:
    - value (str): The input value.

    Returns:
    - str: The processed value.
    """
    if value == "NULL":
        return "NULL"
    else:
        return "'{}'".format(value)



def fetch_data(query):
    """
    Fetches data from the database based on the provided SQL query.
    
    Args:
    - query (str): SQL query to fetch data.
    
    Returns:
    - list: List of tuples containing the fetched data, or None if an error occurs.
    """

    db_addr = dir_and_data_getters.get_credentials('DB_ADDRESS')
    db_user = dir_and_data_getters.get_credentials('DB_USER')
    db_psw = dir_and_data_getters.get_credentials('DB_PWD')
    db_name = dir_and_data_getters.get_credentials('DB_NAME')

    db = DataBaseHandler(db_addr, db_user, db_psw, db_name)
    
    db.connect()

    result = db.fetch(query)
    db.disconnect()

    return result



def get_last_id():
    """
    Retrieves the last inserted ID from the 'transaction' table in the database.
    
    Returns:
    - int: Last inserted ID.
    """
    query = "SELECT MAX(id) FROM transaction;"
    result = fetch_data(query)

    if result is not None:
        return result[0][0]
    else:
        if init_db():
            return get_last_id()



def init_db():
    """
    Initializes the database with a default transaction entry.
    
    Returns:
    - bool: True if initialization is successful, False otherwise.
    """
    db_addr = dir_and_data_getters.get_credentials('DB_ADDRESS')
    db_user = dir_and_data_getters.get_credentials('DB_USER')
    db_psw = dir_and_data_getters.get_credentials('DB_PWD')
    db_name = dir_and_data_getters.get_credentials('DB_NAME')

    db = DataBaseHandler(db_addr, db_user, db_psw, db_name)

    db.connect()

    query = []
    query.append("INSERT INTO transaction (date, total, receipt_ID, receipt_file_name) VALUES (NULL, NULL, NULL, NULL);")


    if db.execute_querys(query):
        return True
    else: 
        return False
    

