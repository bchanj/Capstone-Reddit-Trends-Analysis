#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "models"))

import gspread
import datetime
import os
import base64
import json
import dotenv
import sys
from typing import List, Dict
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from deal import Deal

class GSClient():
    def __init__(self):
        self.contributors: List[str] = [
            "cs2215trends@gmail.com",
            # include additional contributors by email
            # to share document with them
        ]
        # If modifying these scopes, delete the file token.json.
        self._scope: List[str] = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

        dotenv.load_dotenv()
        encrypted_creds: str = os.environ["GSPREAD_CREDS"]
        decoded: bytes = base64.b64decode(encrypted_creds)
        json_dict = json.loads(decoded)
        
        self.gspread_client = gspread.service_account_from_dict(json_dict)

        self.ROW_START = 1
        self.COL_START = 1

    def getSheetLink(self, sheet_title: str) -> str:
        """Returns a link to a spreadsheet that has already been created

        Args:
            sheet_title ([type]): Name of the sheet as a string

        Returns:
            str: Returns the sheet link if it is found else None

        Unit Tests:
            >>> client = GSClient()
            >>> client.createSheet("Test") != None
            True
            >>> client.getSheetLink("Test") != None
            True
            >>> client.getSheetLink("SpreadsheetNotFound") == None
            True
        """
        try:
            sheet: gspread.models.Spreadsheet = self.gspread_client.open(sheet_title)
            return sheet.url
        except:
            pass
        return None

    def createSheet(self, sheet_title: str) -> str:
        """Returns a link to the spreadsheet that is created

        Args:
            title (str, optional): Optional title for the spreadsheet. Defaults to preformatted datetime string for the current day - datetime.datetime.now().strftime("%m-%d-%Y").

        Returns:
            str: Link to the created spreadsheet. The link also contains the key for the spreadsheet. It can be parsed.
        
        Unit Tests:
            >>> client = GSClient()
            >>> link = client.createSheet("Test")
            >>> len(link) != 0
            True
            >>> link = client.createSheet("Test")
            >>> len(link) != 0
            True
        """
        try:
            sheet: gspread.models.Spreadsheet = self.gspread_client.open(sheet_title)
        except:
            sheet: gspread.models.Spreadsheet = self.gspread_client.create(sheet_title)
            for email in self.contributors:
                sheet.share(email, perm_type='user', role='owner')
        finally:
            sheet: gspread.models.Spreadsheet = self.gspread_client.open(sheet_title)
            return sheet.url

    def createWorksheet(self, sheet_link: str, wksht_title: str=datetime.datetime.now().strftime("%m-%d-%Y")) -> None:
        """Create a new worksheet under parent spreadsheet

        Args:
            sheet_link (str): Link to the parent spreadsheet
            wksht_title (str, optional): Title of the worksheet. Defaults to formatted datetime for NOW -> datetime.datetime.now().strftime("%m-%d-%Y").

        Returns:
            str: A link to the newly created spreadsheet

        Unit Tests:
            >>> client = GSClient()
            >>> link = client.createSheet("Test")
            >>> client.createWorksheet(link, "TestWorksheet")
            >>> worksheet_list = client.gspread_client.open_by_url(link).worksheets()
            >>> "TestWorksheet" in [ worksheet.title for worksheet in worksheet_list]
            True
            >>> link = client.createSheet("Test")
            >>> client.createWorksheet(link, "TestWorksheet")
            >>> worksheet_list = client.gspread_client.open_by_url(link).worksheets()
            >>> "TestWorksheet" in [ worksheet.title for worksheet in worksheet_list]
            True
        """
        sheet: gspread.models.Spreadsheet = self.gspread_client.open_by_url(sheet_link)
        try:
            worksheet = sheet.worksheet(wksht_title)
        except:
            worksheet = sheet.add_worksheet(title=wksht_title, rows=0, cols=0)

    def appendToSheet(self, deals: List[Deal], sheet_link: str, wksht_title: str=datetime.datetime.now().strftime("%m-%d-%Y")) -> None:
        """Append new data rows to a sheet.

        Args:
            sheet_link (str): A link to the Google Sheet. See -> getSheet()
            data (List[Deal]): A list of data rows to append to the Google spreadsheet.

        Unit Tests:
            >>> client = GSClient()
            >>> link = client.createSheet("Test")
            >>> client.createWorksheet(link, "TestWorksheet")
            >>> deals = [Deal(subreddit="r/GameDeals", title="50% off Halo Infinite Gear", date="1/2/2022"),Deal(subreddit="r/MUAOnTheCheap", title="FREE Makeup if you promote X company", date="1/11/2022"),Deal(subreddit="r/ThisDoesntExistYet", title="50% off Halo Infinite Gear", date="1/11/2022")]
            >>> client.appendToSheet(deals, link, "TestWorksheet")
            >>> worksheet = client.gspread_client.open_by_url(link).worksheet("TestWorksheet")
        """
        # sheet: gspread.models.Spreadsheet = self.gspread_client.open_by_url(sheet_link)
        self.createWorksheet(sheet_link=sheet_link, wksht_title=wksht_title)
        worksheet: gspread.models.Spreadsheet.worksheet = self.gspread_client.open_by_url(sheet_link).worksheet(wksht_title)
        # Update/Write headers to the spreadsheet
        # Enumerate over attributes in Deal object to create header
        for index, attribute in enumerate(vars(deals[0]).keys()):
            worksheet.update_cell(self.ROW_START, self.COL_START + index, attribute)
        
        worksheet.append_rows([[ value for value in vars(deal).values() if type(value) == str] for deal in deals])

    def dumpDeals(self, deals: List[Deal]):
        """Batch write a list of deals to Google spreadsheets

        Args:
            deals (List[Deal]): List of deals ->
                subreddit attribute for each deal is REQUIRED for successful write 

        Unit Tests:
            # Test that a list of deals with different dates are written to the correct spreadsheets
            >>> client = GSClient()
            >>> link = client.createSheet("Test")
            >>> deals = [Deal(subreddit="r/GameDeals", title="50% off Halo Infinite Gear", date="1/2/2022"), Deal(subreddit="r/MUAOnTheCheap", title="FREE Makeup if you promote X company", date="1/11/2022"), Deal(subreddit="r/ThisDoesntExistYet", title="50% off Halo Infinite Gear", date="1/11/2022")]
            >>> client.dumpDeals(deals)
            >>> worksheets = [ client.gspread_client.open(deal.subreddit).worksheet(deal.date) for deal in deals ]
        """

        # cache the worksheets to avoid unecessary requests to gspread API
        # key: subreddit name
        # value: Sheet value as defined by gspread models
        worksheetCache: Dict[str, gspread.models.Spreadsheet] = {}
        for deal in deals:
            # skip the deal if cached
            if deal.subreddit in worksheetCache:
                continue
            try:
                worksheetCache[deal.subreddit] = self.gspread_client.open(deal.subreddit)
            except:
                self.createSheet(deal.subreddit)
            finally:
                worksheetCache[deal.subreddit] = self.gspread_client.open(deal.subreddit)

        # Write deals
        for deal in deals:
            self.appendToSheet([deal], worksheetCache[deal.subreddit].url, deal.date)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

