#pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib gspread

import gspread
import numpy as np
from google.oauth2.service_account import Credentials
from src.utils import dir_and_data_getters

class GoogleServicesHandler:
    def __init__(self, sheet_name: str = None, sheet_key: str = None):

        if sheet_name is None and sheet_key is None:
            exit('Error: sheet_name or sheet_key must be provided')

        self.scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
        self.creds = Credentials.from_service_account_file(dir_and_data_getters.get_current_dir() + "/../configs/google-credentials.json", scopes=self.scope)
        self.client = gspread.authorize(self.creds)
        
        if sheet_name is not None:
            self.workbook = self.client.open(sheet_name)
        else:
            self.workbook = self.client.open_by_key(sheet_key)


    def get_sheet(self, sheet_name: str):
        return self.workbook.worksheet(sheet_name)
    

    def update_sheet(self, sheet_name: str, start: list, values: list):
        sheet = self.get_sheet(sheet_name)

        num_rows = len(values)
        num_cols = len(values[0])

        # Calcola le coordinate dell'angolo superiore sinistro e dell'angolo inferiore destro
        start_row = start[0]
        start_col = start[1]
        end_row = start_row + num_rows - 1
        end_col = start_col + num_cols - 1

        # Genera l'intervallo di celle
        cell_range = f"{column_index_to_letter(start_col)}{start_row}:{column_index_to_letter(end_col)}{end_row}"
        cells = sheet.range(cell_range)

        print('cell_range= ' + cell_range)
        print(cells)
    
        arr = []
        for row in values:
            for cell in row:
                arr.append(cell)

        for i, cell in enumerate(cells):
            cell.value = str(arr[i])
            print (str(i) + '  ' + cell.value)
        
        sheet.update_cells(cells)


    def append_to_sheet(self, sheet_name: str, values: list):
        sheet = self.get_sheet(sheet_name)
        sheet.append_rows(values)

def column_index_to_letter(index):
    """Converti l'indice numerico della colonna in una lettera corrispondente."""
    letters = ''
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters



def paste_matrix(matrix: list, SHEET_KEY: str, start_r: int, start_c: int):
    start = [start_r, start_c]

    print('key= '+ SHEET_KEY)
    gsh = GoogleServicesHandler(None, SHEET_KEY)

    gsh.update_sheet('sos', start, matrix)


