import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'cosmos', 'models'))

import logging

import azure.functions as func
from cosmos_db_wrapper import CosmosClientWrapper
from typing import Dict, List
from collections import defaultdict

def main(req: func.HttpRequest) -> func.HttpResponse:
    def createTable(data: Dict[str, List[str]]):
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
        html = '<table><tr><th>' + '</th><th>'.join(data.keys()) + '</th></tr>'

        for row in zip(*data.values()):
            html += '<tr><td>' + '</td><td>'.join(row) + '</td></tr>'

        html += '</table>'

        return html

    try:
        logging.info('Python HTTP trigger function processed a request.')
        cosmosDbWrapper = CosmosClientWrapper()
        extract = cosmosDbWrapper.readEntries()
        res = defaultdict(list)
        for sub in extract:
            for key in sub:
                res[key].append(sub[key])
        data = createTable(res)
        preamble = open("table_template.html").read()
        table = open("table_template.html").read().format(table_contents=data)
        print(preamble + table)
        return func.HttpResponse(
            status_code=200,
            headers={'content-type':'text/html'}, 
            body=(preamble+table))
    except (e):
        message=f"Internal Server Error: {e}"
        logging.info(message)
        return func.HttpResponse(
             status_code=500,
             
        )