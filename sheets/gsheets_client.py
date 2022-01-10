import gspread
import datetime
import os.path

from typing import List, Dict
from pathlib import Path
from google.oauth2.service_account import Credentials

from models.deal import Deal

class GSClient():
    def __init__(self):
        self.contributors = [
            "cs2215trends@gmail.com",
            # include additional contributors by email
            # to share document with them
        ]
        # If modifying these scopes, delete the file token.json.
        self._scope: List[str] = ['https://spreadsheets.google.com/feeds',
                                  'https://www.googleapis.com/auth/drive']
        # create Google API Credentials from service_credentials found in parent directory
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('service_credentials.json'):
            creds = Credentials.from_service_account_file(
                Path(__file__).parents[0] / "service_credentials.json", scopes=self._scope)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        self.gspread_client = gspread.authorize(creds)

        self.ROW_START = 1
        self.COL_START = 0

    def createSheet(self, sheet_title: str) -> str:
        """Returns a link to the spreadsheet that is created

        Args:
            title (str, optional): Optional title for the spreadsheet. Defaults to preformatted datetime string for the current day - datetime.datetime.now().strftime("%m-%d-%Y").

        Returns:
            str: Link to the created spreadsheet. The link also contains the key for the spreadsheet. It can be parsed.
        """
        id: str = self.gspread_client.create(sheet_title)
        sheet: gspread.models.Spreadsheet = self.gspread_client.open_by_key(id)
        for email in self.contributors:
            sheet.share(emails, perm_type='user', role='owner')
        return "https://docs.google.com/spreadsheets/d/%s" % sheet.id

    def createWorksheet(self, sheet_link: str, wksht_title: str=datetime.datetime.now().strftime("%m-%d-%Y")) -> None:
        """Create a new worksheet under parent spreadsheet

        Args:
            sheet_link (str): Link to the parent spreadsheet
            wksht_title (str, optional): Title of the worksheet. Defaults to formatted datetime for NOW -> datetime.datetime.now().strftime("%m-%d-%Y").

        Returns:
            str: A link to the newly created spreadsheet
        """
        sheet: gspread.models.Spreadsheet = self.gspread_client.open_by_url(sheet_link)
        worksheet = sheet.add_worksheet(title=wksht_title)

    def appendToSheet(self, data: List[Deal], sheet_link: str, wksht_title: str=datetime.datetime.now().strftime("%m-%d-%Y")) -> None:
        """Append new data rows to a sheet.

        Args:
            sheet_link (str): A link to the Google Sheet. See -> getSheet()
            data (List[Deal]): A list of data rows to append to the Google spreadsheet.
        """
        sheet: gspread.models.Spreadsheet = self.gspread_client.open_by_url(sheet_link)
        worksheet = sheet.worksheet(wksht_title)
        # Update/Write headers to the spreadsheet
        worksheet.delete_row(self.ROW_START)
        # Enumerate over attributes in Deal object to create header
        for index, attribute in enumerate(vars(deal).keys()):
            worksheet.update_cell(self.ROW_START, index, attribute)

        # Find the first available row to write data into:
        row: int = self.ROW_START
        while worksheet.row_values(row).empty():
            row += 1
        
        # iterate over all given objects
        for deal in deals: 
            # iterate over object properties
            col: int = self.COL_START
            for attribute, value in vars(deal):
                worksheet.update_cell(row, col, value)
                col += 1
