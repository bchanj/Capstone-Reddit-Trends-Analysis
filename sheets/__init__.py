import sys
import os

from sheets.models.gsheets_client import GSClient
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))
import logging
# Figure out how to import gsheets
import azure.functions as func
from deal import Deal

# Research input format for this function, created template from cosmosDBTrigger
def main(documents: func.DocumentList) -> str: 
    # Out of this list of json objects, get one of them
    result = [] # List of json objects -> deal objects
    g = GSClient()
    for item in documents: # Format the json information into deal object
        excluding_private = {x: item[x] for x in item if not x.startswith("_")}
        result.append(Deal(**excluding_private))
    g.dumpDeals() # Call dumpDeals
    if documents:
        logging.info('Document id: %s', documents[0]['id'])