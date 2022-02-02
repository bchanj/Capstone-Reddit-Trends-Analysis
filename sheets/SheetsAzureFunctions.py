import os
import sys
sys.path.append(os.path.dirname(__file__))
from models import gsheets_client
from cgi import test
from importlib.resources import path
from os.path import exists
from pathlib import Path
import azure.functions as func
import glob
import json
import logging

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
        jsonObject = {"link" : response}
        return func.HttpResponse(
            json.dumps(jsonObject),
            mimetype="application/json"
        )

    elif function == "createSheet":
        sheet = gsheets_client.GSClient()
        sheet_title = req.params.get('sheet_title')
        response = sheet.createSheet(sheet_title)
        jsonObject = {"link" : response}
        return func.HttpResponse(
            json.dumps(jsonObject),
            mimetype="application/json"
        )

    elif function == "createWorksheet":
        sheet = gsheets_client.GSClient()
        sheet_link = req.params.get('sheet_link')
        wksht_title = req.params.get('wksht_title')
        response = sheet.createWorksheet(sheet_link, wksht_title)

        #Does not work yet, GSheet function needs to return a response 
        jsonObject = {"link" : response}
        return func.HttpResponse(
            json.dumps(jsonObject),
            mimetype="application/json"
        )

    elif function == "appendToSheet":
        sheet = gsheets_client.GSClient()
        sheet_link = req.params.get('sheet_link')
        data = req.params.get('data')
        response = sheet.appendToSheet(sheet_link, data)

        #Does not work yet, GSheet function needs to return a response 
        jsonObject = {"link" : response}
        return func.HttpResponse(
            json.dumps(jsonObject),
            mimetype="application/json"
        )

    elif function == "dumpDeals":
        sheet = gsheets_client.GSClient()
        deals = req.params.get('deals')
        response = sheet.dumpDeals(deals)

        #Does not work yet, GSheet function needs to return a response 
        jsonObject = {"link" : response}
        return func.HttpResponse(
            json.dumps(jsonObject),
            mimetype="application/json"
        )
    
    else:
        jsonObject = {"link" : "The Sheets Function works but wrong parameters have been passed!"}
        return func.HttpResponse(
            json.dumps(jsonObject),
            mimetype="application/json"
        )
