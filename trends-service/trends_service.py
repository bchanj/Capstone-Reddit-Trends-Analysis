import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'cosmos', 'models'))

import logging
import json
import azure.functions as func
from cosmos_db_wrapper import CosmosClientWrapper
from query_filter import QueryFilter
from typing import Dict, List
from collections import defaultdict

def main(req: func.HttpRequest) -> func.HttpResponse:
    def createTable(data: Dict[str, List[str]]):
        """Creates `an HTML table template
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


    start: int = req.params.get("start")
    if start is None:
        start = 0
        
    limit: int = req.params.get("limit")
    if limit is None:
        limit = 10

    filters: List[QueryFilter] = []
    for key, value in req.params.items():
        if key == "start" or key == "limit":
            continue
        filters.append(QueryFilter(key, value))
    
    if not filters:
        filters = None


    cosmosDbWrapper = CosmosClientWrapper()
    extract = cosmosDbWrapper.readEntries(start=start, limit=limit, filters=filters)

    data = []
    # res = defaultdict(list)
    for deal in extract:
        dealDict = {x: deal.__dict__[x] for x in deal.__dict__ if x not in ["subreddit", "synonyms", "bundle_id", "bundle_title", "merchant", "id", "price_eur", "price_gbp"]}
        dealDict = {
            "title": dealDict["title"],
            "discount": dealDict["discount"],
            "price": dealDict["price"],
            "url": dealDict["url"]
        }
        data.append(dealDict)
        # for k, v in dealDict.items():
        #     res[k].append(v)

    
    return func.HttpResponse(
        status_code=200,
        headers={
            'content-type':'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        charset='utf-8',
        body=json.dumps(data)
    )

    # data = createTable(res)
    
    # parent_dir = os.path.dirname(__file__)
    # preamble = open(os.path.join(parent_dir, "preamble.html")).read()
    # table = open(os.path.join(parent_dir, "table_template.html")).read().format(table_contents=data)
    # return func.HttpResponse(
    #     status_code=200,
    #     headers={'content-type':'text/html'},
    #     charset="utf-16",
    #     # charset='utf-16',
    #     body=(preamble+table)
    # )
