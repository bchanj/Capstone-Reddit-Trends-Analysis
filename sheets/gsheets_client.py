import gspread
import datetime
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

    def createSheet(self, parent_folder: str, title: str=datetime.datetime.now().strftime("%m-%d-%Y")) -> str:
        """Returns a link to the spreadsheet that is created

        Args:
            parent_folder_ids (str): Link to the parent folder for the spreadsheet. Spreadsheets must have a parent folder.
            title (str, optional): Optional title for the spreadsheet. Defaults to preformatted datetime string for the current day - datetime.datetime.now().strftime("%m-%d-%Y").

        Returns:
            str: Link to the created spreadsheet. The link also contains the key for the spreadsheet. It can be parsed.
        """
        id: str = self.client.create(title)
        sheet: gspread.models.Spreadsheet = self.client.open_by_key(id)
        for email in self.contributors:
            sheet.share(emails, perm_type='user', role='owner')
        return id

    def createFolder(self, title: str) -> str:
        pass

    def getSheet(self, parent_folder: str, title: str) -> str:
        """Get spreadsheet link with parent folder link and spreadsheet title.

        Args:
            parent_folder (str): Link to the parent folder
            title (str): The title of the spreadsheet.

        Returns:
            str: A link to the spreadsheet found by the title provided.
        """
        pass

    def appendToSheet(self, sheet_link: str, data: List[Deal]) -> None:
        """Append new data rows to a sheet.

        Args:
            sheet_link (str): A link to the Google Sheet. See -> getSheet()
            data (List[Deal]): A list of data rows to append to the Google spreadsheet.
        """
        sheet = self.open(id)
