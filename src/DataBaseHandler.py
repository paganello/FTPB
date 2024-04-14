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
            cursor.execute(query)

        if self.connection.commit():
            cursor.close()
            return True
        
        else:
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
    
    # Get the last ID
    def get_last_id(self):
        query = "SELECT MAX(id) FROM transations;"
        result = self.fetch_data(query)
        return result[0][0]


def update(jsons, img_name=None):
    db = DataBaseHandler(db_addr="localhost", db_user="PersonalFinanceBot_user", db_psw="prova123", db_name="PersonalFinanceBot")
    db.connect()

    querys = create_query_array(db, jsons, img_name)

    if db.execute_querys(querys):
        db.disconnect()
        return True
    
    else:
        db.disconnect()
        return False
    

def create_query_array(db, jsons, img_name=None):

    s = json.dumps(json_file)
    json_file = json.loads(s)
        
    querys = []

    for json_file in jsons:

        if "date" in json_file and "total" in json_file and "recipt_ID" in json_file:

            if img_name:
                querys.append("INSERT INTO transation (date, total, receipt_ID, recipt_file_name) VALUES ('{}', '{}', '{}', '{}');".format(json_file["date"], json_file["total"], json_file["receipt_ID"], img_name)) 
                
            else:
                querys.append("INSERT INTO transation (date, total, receipt_ID, recipt_file_name) VALUES ('{}', '{}', '{}', 'NULL');".format(json_file["date"], json_file["total"], json_file["receipt_ID"]))

                
        transaction_ID = db.get_last_id()

        if "amount" in json_file and "tax" in json_file and "description" in json_file:
            
            querys.append("INSERT INTO articles (transaction_ID, amount, tax, description) VALUES ('{}', '{}', '{}', '{}');".format(transaction_ID, json_file["amount"], json_file["tax"], json_file["description"]))

        if "name" in json_file and "address" in json_file and "city" in json_file and "VAT" in json_file:
                
            querys.append("INSERT INTO store (transaction_ID, name, address, city, VAT) VALUES ('{}', '{}', '{}', '{}', '{}');".format(transaction_ID, json_file["name"], json_file["address"], json_file["city"], json_file["VAT"]))


    return querys


def fetch_data(query):
    db = DataBaseHandler(db_addr="localhost", db_user="PersonalFinanceBot_user", db_psw="prova123", db_name="PersonalFinanceBot")
    db.connect()

    result = db.fetch_data(query)
    db.disconnect()

    return result