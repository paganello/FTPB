import mysql.connector
import json

class DataBaseHandler:
    
    def __init__(self, db_psw, db_addr, db_user, db_name):
        self.db_psw = db_psw
        self.db_user = db_user
        self.db_addr = db_addr
        self.db_name = db_name
        self.connection = None
    
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
    
    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, json_file):

        s = json.dumps(json_file)
        json_file = json.loads(s)
        
        try: 

            cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            return False
        
        try:
            print (len(json_file))

            if len(json_file) == 2 and "date" in json_file and "total" in json_file:
                query = "INSERT INTO transations (date, total) VALUES ('{}', '{}');".format(json_file["date"], json_file["total"])
                print (query)
                cursor.execute(query)
            
            
            if len(json_file) == 3 and "amount" in json_file and "tax" in json_file and "description" in json_file:
                id = self.get_last_id()
                query = "INSERT INTO articles_in_transations (ID, amount, tax, description) VALUES ('{}', '{}', '{}', '{}');".format(id, json_file["amount"], json_file["tax"], json_file["description"])
                print (query)
                cursor.execute(query)
        
            self.connection.commit()
            return True

        except mysql.connector.Error as err:
            self.connection.rollback()
            return False

        finally:
            cursor.close()


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
    
    def get_last_id(self):
        query = "SELECT MAX(id) FROM transations;"
        result = self.fetch_data(query)
        return result[0][0]


def update(json_file):
    db = DataBaseHandler(db_addr="localhost", db_user="PersonalFinanceBot_user", db_psw="prova123", db_name="PersonalFinanceBot")
    db.connect()

    if db.execute_query(json_file):
        db.disconnect()
        return True
    else:
        db.disconnect()
        return False
    
    
def fetch_data(query):
    db = DataBaseHandler(db_addr="localhost", db_user="PersonalFinanceBot_user", db_psw="prova123", db_name="PersonalFinanceBot")
    db.connect()

    result = db.fetch_data(query)
    db.disconnect()

    return result