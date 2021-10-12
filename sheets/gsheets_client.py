import gspread
from typing import List
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
        creds = Credentials.from_service_account_file(
            Path(__file__).parents[0] / "service_credentials.json", scopes=self._scope)
        self.client = gspread.authorize(creds)

    # Returns the id of the spreadsheet that is created
    # post-conditions: shares spreadsheets with contributors
    def create(self, title: str) -> str:
        id: str = self.client.create(title)
        sheet: gspread.models.Spreadsheet = self.client.open_by_key(id)
        sheet.share(emails, perm_type='user', role='owner')
        return id

    def open(self, id: int) -> gspread.models.Spreadsheet:
        sheet: gspread.models.Spreadsheet = self.client.open_by_key(id)
        return sheet

    def append(self, id: int, data: Deal) -> None:
        sheet = self.open(id)
