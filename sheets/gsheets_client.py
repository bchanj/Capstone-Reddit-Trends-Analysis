import gspread
import datetime
import os.path

from typing import List, Dict
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from sheets.models.deal import Deal

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

        self.gspread_client = gspread.service_account()

        self.ROW_START = 1
        self.COL_START = 1

    def getSheetLink(self, sheet_title) -> str:
        """Returns a link to a spreadsheet that has already been created

        Args:
            sheet_title ([type]): Name of the sheet as a string

        Returns:
            str: Returns the sheet link if it is found else None
        """
        try:
            sheet: gspread.models.Spreadsheet = self.gspread_client.open(sheet_title)
            return sheet.url
        except gspread.SpreadsheetNotFound:
            pass
        return None
        

    def createSheet(self, sheet_title: str) -> str:
        """Returns a link to the spreadsheet that is created

        Args:
            title (str, optional): Optional title for the spreadsheet. Defaults to preformatted datetime string for the current day - datetime.datetime.now().strftime("%m-%d-%Y").

        Returns:
            str: Link to the created spreadsheet. The link also contains the key for the spreadsheet. It can be parsed.
        """
        sheet: gspread.models.Spreadsheet = self.gspread_client.create(sheet_title)
        for email in self.contributors:
            sheet.share(email, perm_type='user', role='owner')
        return sheet.url

    def createWorksheet(self, sheet_link: str, wksht_title: str=datetime.datetime.now().strftime("%m-%d-%Y")) -> None:
        """Create a new worksheet under parent spreadsheet

        Args:
            sheet_link (str): Link to the parent spreadsheet
            wksht_title (str, optional): Title of the worksheet. Defaults to formatted datetime for NOW -> datetime.datetime.now().strftime("%m-%d-%Y").

        Returns:
            str: A link to the newly created spreadsheet
        """
        sheet: gspread.models.Spreadsheet = self.gspread_client.open_by_url(sheet_link)
        try:
            worksheet = sheet.worksheet(wksht_title)
        except:
            worksheet = sheet.add_worksheet(title=wksht_title, rows=10, cols=10)

    def appendToSheet(self, deals: List[Deal], sheet_link: str, wksht_title: str=datetime.datetime.now().strftime("%m-%d-%Y")) -> None:
        """Append new data rows to a sheet.

        Args:
            sheet_link (str): A link to the Google Sheet. See -> getSheet()
            data (List[Deal]): A list of data rows to append to the Google spreadsheet.
        """
        sheet: gspread.models.Spreadsheet = self.gspread_client.open_by_url(sheet_link)
        worksheet = sheet.worksheet(wksht_title)
        # # Update/Write headers to the spreadsheet
        worksheet.delete_rows(self.ROW_START, self.ROW_START) 
        # Enumerate over attributes in Deal object to create header
        for index, attribute in enumerate(vars(deals[0]).keys()):
            worksheet.update_cell(self.ROW_START, index + 1, attribute)
        
        worksheet.append_rows([list(vars(deal).values()) for deal in deals])


    # TEST WITH
    # [
    #     Deal(subreddit=="r/GameDeals", title="50% off Halo Infinite Gear", date="1/2/2022"),
    #     Deal(subreddit=="r/MUAOnTheCheap", title="FREE Makeup if you promote X company", date="1/11/2022"),
    #     Deal(subreddit=="r/ThisDoesntExistYet", title="50% off Halo Infinite Gear", date="1/11/2022"),
    # ]
    def dumpDeals(self, deals: List[Deal]):
        """Batch write a list of deals to Google spreadsheets

        Args:
            deals (List[Deal]): List of deals ->
                subreddit attribute for each deal is REQUIRED for successful write 
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
                worksheetCache[deal.subreddit] = gspread.models.open(deal.subreddit)
            except:
                self.createSheet(deal.subreddit)
            finally:
                worksheetCache[deal.subreddit] = gspread.models.open(deal.subreddit)

        # Write deals
        for deal in deals:
            self.appendToSheet([deal], worksheetCache[deal.subreddit].url, deal.date)

