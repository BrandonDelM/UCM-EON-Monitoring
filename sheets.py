import gspread
from gspread import Client, Spreadsheet, Worksheet
from google.oauth2.service_account import Credentials

def init_sheets_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets"
    ]
    creds  = Credentials.from_service_account_file("./keys/credentials-google.json", scopes=scopes)
    client = gspread.authorize(creds)
    return client

def get_sheet(client: Client, id):
    return client.open_by_key(id)

def get_worksheets(sheet: Spreadsheet):
    return sheet.worksheets()

def get_worksheet_columns(worksheet: Worksheet):
    data = worksheet.get_all_values()
    rows = data[1:]

    urls = [row[0] for row in rows]

    return urls