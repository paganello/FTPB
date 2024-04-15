import mysql.connector
import json

class DataBaseHandler:
    
    # Constructor
    def __init__(self, db_psw, db_addr, db_user, db_name):
        self.db_psw = db_psw
        self.db_user = db_user
        self.db_addr = db_addr
        self.db_name = db_name
        self.connection = None
    
    # Connect to the DB
    def connect(self):
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
    
    # Disconnect from the DB
    def disconnect(self):
        if self.connection:
            self.connection.close()

    # Execute a query
    def execute_querys(self, querys):
        
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
        
    # Fetch data
    def fetch_data(self, query):
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
    db = DataBaseHandler(db_addr="localhost", db_user="PersonalFinanceBot_user", db_psw="prova123", db_name="PersonalFinanceBot")
    db.connect()

    result = db.fetch_data(query)
    db.disconnect()

    return result


def get_last_id():
    query = "SELECT MAX(id) FROM transaction;"
    result = fetch_data(query)

    if result is not None:
        return result[0][0]
    else:
        if init_db():
            return get_last_id()

        

def init_db():
    db = DataBaseHandler(db_addr="localhost", db_user="PersonalFinanceBot_user", db_psw="prova123", db_name="PersonalFinanceBot")
    db.connect()

    query = []
    query.append("INSERT INTO transaction (date, total, receipt_ID, receipt_file_name) VALUES (NULL, NULL, NULL, NULL);")

    print(query)

    if db.execute_querys(query):
        return True
    else: 
        return False



