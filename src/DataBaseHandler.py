import mysql.connector
import json

class DataBaseHandler:
    
    def __init__(self, db_psw, db_addr, db_user, db_name):
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

            try: 
                cursor.execute(query)
                print(query)

            except mysql.connector.Error as err:
                cursor.close()
                return False

        try: 
            self.connection.commit()
            cursor.close()

            return True
        
        except mysql.connector.Error as err:
            cursor.close()
            return False
        
    
    def fetch_data(self, query):
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
    db = DataBaseHandler(db_addr="localhost", db_user="PersonalFinanceBot_user", db_psw="prova123", db_name="PersonalFinanceBot")
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
    querys = []
    transaction_ID = None

    for json_file in jsons:

        if "date" in json_file and "total" in json_file and "receipt_ID" in json_file:

            if img_name:
                querys.append("INSERT INTO transaction (date, total, receipt_ID, receipt_file_name) VALUES ('{}', '{}', '{}', '{}');".format(json_file["date"], json_file["total"], json_file["receipt_ID"], img_name)) 
            else:
                querys.append("INSERT INTO transaction (date, total, receipt_ID, receipt_file_name) VALUES ('{}', '{}', '{}', 'NULL');".format(json_file["date"], json_file["total"], json_file["receipt_ID"]))

            return querys
        
        if "amount" in json_file and "tax" in json_file and "description" in json_file:
            if transaction_ID is None:
                transaction_ID = get_last_id()
            querys.append("INSERT INTO good (transaction_ID, amount, tax, description) VALUES ('{}', '{}', '{}', '{}');".format(transaction_ID, json_file["amount"], json_file["tax"], json_file["description"]))

        if "name" in json_file and "address" in json_file and "city" in json_file and "VAT" in json_file:
            if transaction_ID is None:
                transaction_ID = get_last_id()
            querys.append("INSERT INTO store (transaction_ID, name, address, city, VAT) VALUES ('{}', '{}', '{}', '{}', '{}');".format(transaction_ID, json_file["name"], json_file["address"], json_file["city"], json_file["VAT"]))

    return querys



def fetch_data(query):
    """
    Fetches data from the database based on the provided SQL query.
    
    Args:
    - query (str): SQL query to fetch data.
    
    Returns:
    - list: List of tuples containing the fetched data, or None if an error occurs.
    """
    db = DataBaseHandler(db_addr="localhost", db_user="PersonalFinanceBot_user", db_psw="prova123", db_name="PersonalFinanceBot")
    db.connect()

    result = db.fetch_data(query)
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
    db = DataBaseHandler(db_addr="localhost", db_user="PersonalFinanceBot_user", db_psw="prova123", db_name="PersonalFinanceBot")
    db.connect()

    query = []
    query.append("INSERT INTO transaction (date, total, receipt_ID, receipt_file_name) VALUES (NULL, NULL, NULL, NULL);")

    print(query)

    if db.execute_querys(query):
        return True
    else: 
        return False
