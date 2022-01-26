from cgi import test
from importlib.resources import path
import logging
import os
import sys
import azure.functions as func
from pathlib import Path
from os.path import exists
import glob
from .models import gsheets_client

dir_path = os.path.dirname(os.path.realpath(__file__))
filex = glob.glob(dir_path + '/**/*', recursive=True)
files = ""
for x in filex:
    files += x + "\n"
print(files)
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    function = req.params.get('function')
    if not function:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            function = req_body.get('function')
    if function == "getSheetLink":
        sheet = gsheets_client.GSClient()
        sheet_title = req.params.get('sheet_title')
        response = sheet.getSheetLink(sheet_title)
        if response:
            return func.HttpResponse(response)
        else:
            return func.HttpResponse("Unable to retrieve sheet link!")

    elif function == "createSheet":
        sheet = gsheets_client.GSClient()
        sheet_title = req.params.get('sheet_title')
        response = sheet.createSheet(sheet_title)
        if response:
            return func.HttpResponse(response)
        else:
            return func.HttpResponse("Unable to create Sheet!")

    elif function == "createWorksheet":
        sheet = gsheets_client.GSClient()
        sheet_link = req.params.get('sheet_link')
        wksht_title = req.params.get('wksht_title')
        response = sheet.createWorksheet(sheet_link, wksht_title)
        
        #Does not work yet, GSheet function needs to return a response 
        if response:
            return func.HttpResponse(response)
        else:
            return func.HttpResponse("Unable to create Worksheet!")

    elif function == "appendToSheet":
        sheet = gsheets_client.GSClient()
        sheet_link = req.params.get('sheet_link')
        data = req.params.get('data')
        response = sheet.appendToSheet(sheet_link, data)

        #Does not work yet, GSheet function needs to return a response 
        if response:
            return func.HttpResponse(response)
        else:
            return func.HttpResponse("Unable to append to sheet!")

    elif function == "dumpDeals":
        sheet = gsheets_client.GSClient()
        deals = req.params.get('deals')
        response = sheet.dumpDeals(deals)

        #Does not work yet, GSheet function needs to return a response 
        if response:
            return func.HttpResponse(response)
        else:
            return func.HttpResponse("Unable to dump deals to sheet!")
    
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
