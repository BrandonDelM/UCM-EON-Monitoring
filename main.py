from automation import Automation, create_checker
from sheets import *

def start_automation():
    client: Client = init_sheets_client()
    sheet: Spreadsheet = get_sheet(client, "10JOd0s1Y7q8BqbInpZ15dvomEIz6402KtDUpSj7g7Rk")
    automators: list[Automation] = []
    worksheets: list[Worksheet] = get_worksheets(sheet)
    for worksheet in worksheets:
        url, table = get_worksheet_columns(worksheet)
        checker = create_checker(worksheet.title.lower(), url)
        automators.append(Automation(
            checker=checker,
            table=table
        ))
    for automator in automators:
        automator.automate()

if __name__ == "__main__":
    start_automation()