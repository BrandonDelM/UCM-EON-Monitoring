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
    tables = [row[1] for row in rows]

    return urls, tables

from datetime import date
def update_worksheet_logs(worksheet, updates, url):
    if len(updates) != 0:
        update_log = f"{date.today()}: New updates for {url}\n"
        for update in updates:
            update_log += f"{update}\n"
        update_log = update_log[:49000]
        worksheet.append_row([update_log])