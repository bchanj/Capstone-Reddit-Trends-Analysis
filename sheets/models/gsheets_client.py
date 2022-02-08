import gspread
import datetime
import os
import base64
import json
import dotenv

from typing import List, Dict
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import deal

class Filter():
    def __init__(self, filter_name: str, filter_value: str):
        self.filter_name = filter_name
        self.filter_value = filter_value

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

    def createWorksheet(self, sheet_link: str, wksht_title: str = datetime.datetime.now().strftime("%m-%d-%Y")) -> None:
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

    def appendToSheet(self, deals: List[deal.Deal], sheet_link: str,
                      wksht_title: str = datetime.datetime.now().strftime("%m-%d-%Y")) -> None:
        """Append new data rows to a sheet.

        Args:
            sheet_link (str): A link to the Google Sheet. See -> getSheet()
            data (List[deal.Deal]): A list of data rows to append to the Google spreadsheet.

        Unit Tests:
            >>> client = GSClient()
            >>> link = client.createSheet("Test")
            >>> client.createWorksheet(link, "TestWorksheet")
            >>> deals = [deal.Deal(subreddit="r/Gamedeal.Deals", title="50% off Halo Infinite Gear", date="1/2/2022"),deal.Deal(subreddit="r/MUAOnTheCheap", title="FREE Makeup if you promote X company", date="1/11/2022"),deal.Deal(subreddit="r/ThisDoesntExistYet", title="50% off Halo Infinite Gear", date="1/11/2022")]
            >>> client.appendToSheet(deals, link, "TestWorksheet")
            >>> worksheet = client.gspread_client.open_by_url(link).worksheet("TestWorksheet")
        """
        # sheet: gspread.models.Spreadsheet = self.gspread_client.open_by_url(sheet_link)
        self.createWorksheet(sheet_link=sheet_link, wksht_title=wksht_title)
        worksheet: gspread.models.Spreadsheet.worksheet = self.gspread_client.open_by_url(sheet_link).worksheet(
            wksht_title)
        # Update/Write headers to the spreadsheet
        # Enumerate over attributes in deal.Deal object to create header
        for index, attribute in enumerate(vars(deals[0]).keys()):
            worksheet.update_cell(self.ROW_START, self.COL_START + index, attribute)

        worksheet.append_rows([[value for value in vars(deal).values() if type(value) == str] for deal in deals])

    def dumpDeals(self, deals: List[deal.Deal]) -> None:
        """Batch write a list of deals to Google spreadsheets

        Args:
            deals (List[Deal]): List of deals ->
                subreddit attribute for each deal is REQUIRED for successful write 

        Unit Tests:
            # Test that a list of deals with different dates are written to the correct spreadsheets
            >>> client = GSClient()
            >>> link = client.createSheet("Test")
            >>> deals = [deal.Deal(subreddit="r/GameDeals", title="50% off Halo Infinite Gear", date="1/2/2022"), deal.Deal(subreddit="r/MUAOnTheCheap", title="FREE Makeup if you promote X company", date="1/11/2022"), deal.Deal(subreddit="r/ThisDoesntExistYet", title="50% off Halo Infinite Gear", date="1/11/2022")]
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

    def readSheet(self, sheet_link: str, wksht_title: str = datetime.datetime.now().strftime("%m-%d-%Y")) -> Dict[str, List[str]]:
        """Reads data from a single sheet to create an HTML table

        Args:
            sheet_link (str): A link to the Google Sheet. See -> getSheet()
            wksht_title (str): Title of the worksheet. Defaults to formatted datetime for NOW -> datetime.datetime.now().strftime("%m-%d-%Y").

        Unit Tests: TODO
            # Test that checks the dictionaries and lists are populated correctly

        """
        worksheet: gspread.models.Spreadsheet.worksheet = self.gspread_client.open_by_url(sheet_link).worksheet(wksht_title)
        sheetDict: Dict[str, List[str]] = {}
        # key is column header, list is cells under header
        header: List[str] = worksheet.row_values(self.ROW_START)
        for k in range(len(header)):
            sheetDict[header[k]] = worksheet.col_values(k)[1:]
            # while worksheet.col_values(k) is not None:
            #     col = worksheet.col_values(k)
            #     sheetDict[col(0)] = col.pop()
        # key is column header, list is cells under header
        return sheetDict

    def filterSheetDictionary(self, sheetDict: Dict[str, List[str]], filters: List[Filter]) -> Dict[str, List[str]]:
        """Filters the dictionary based on keyword

        Args:
            sheetDict (dict): A dictionary with the name of the table column as the key, and a list for the table cells

        Unit Tests: TODO
            >>> dict: Dict[str, List[str]] = { "x": ["1", "2"], "y": ["1", "3"] }
            >>> client: GSClient = GSClient()
            >>> filters: List[Filter] = [Filter("x", "1"), Filter("y", "2")]
            >>> client.filterSheetDictionary(dict, filters)
            {"x": [1], "y": [2]}
            >>> dict: Dict[str, List[str]] = { }
            >>> client.filterSheetDictionary(dict, filters)
            { }
            >>> dict: Dict[str, List[str]] = { "z": ["1", "2"], "b": ["1", "3"] }
            >>> client.filterSheetDictionary(dict, filters)
            { "x": ["1", "2"], "y": ["1", "3"] }
            >>> filters: List[Filter] = [Filter("x", "This is not in the dict"), Filter("y", "And so is this")]
            >>> client.filterSheetDictionary(dict, filters)
            { }
        """
        return sheetDict

    def createTable(self, sheetDict: Dict[str, List[str]]):
        """Creates an HTML table template
        TODO at the moment this opens a file and dumps the table code to be copy-paste; will likely need pyppeteer to dump table into email client

        Args:
            sheetDict (dict): A dictionary with the name of the table column as the key, and a list for the table cells

        Unit Tests: TODO
            # Test that a table is created with the correct information inserted
            >>> dict: Dict[str, List[str]] = { "x": ["1", "2"], "y": ["1", "3"] }
            >>> client: GSClient = GSClient()
            >>> client.createTable(dict)
            "<tr><th>x</th><th>y</th></tr><tr><td>1</td><td>1</td></tr><tr><td>2</td><td>3</td></tr>"
        """
        data = ""
        for k, v in sheetDict.items():
            data += "<tr>"
            data += "<th>" + k + "</th>"
            if isinstance(v, list):
                for value in v:
                    data += "<td>" + value + "</td>"
            data += "</tr>"
        table = open("table_template.html").read().format(table_contents=data)
        return table


if __name__ == "__main__":
    import doctest

    doctest.testmod()
