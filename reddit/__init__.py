from cgi import test
from importlib.resources import path
import logging
import os
import sys
import azure.functions as func
from pathlib import Path
from os.path import exists
import glob
from .models import reddit_client


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
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
