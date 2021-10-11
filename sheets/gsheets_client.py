import gspread
from google.oauth2.service_account import Credentials
from typing import List


class Sheets():
    def __init__(self):
        # If modifying these scopes, delete the file token.json.
        self._scope: List[str] = ['https://spreadsheets.google.com/feeds',
                                  'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(
            'service_credentials.json', scopes=self._scope)
        self.gspread_client = gspread.authorize(creds)
