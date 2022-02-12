import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'cosmos', 'models'))

# imports alphabetically sorted
from cgi import test
from importlib.resources import path
from models import reddit_client
from os.path import exists
from pathlib import Path
from unittest import result
from cosmos_db_wrapper import CosmosClientWrapper
from reddit_client import RedditClient, SubredditTarget
import azure.functions as func
import glob
import http
import json
import logging

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        cosmosDbWrapper = CosmosClientWrapper()
        e = cosmosDbWrapper.readEntries()
        print(e)
        # reddit = RedditClient()
        # extract = reddit.getDeals(SubredditTarget.GAMEDEALS)
        # cosmosDbWrapper.createEntries(extract)
        
    except (e):
        logging.info(f"Error: {e}")
        return func.HttpResponse(
             status_code=500
        )

    # if not function:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         function = req_body.get('function')

    # if function == "getHotSubmissions":
    #     subreddit = req.params.get('subreddit')
    #     results = reddit.getNewSubmissions(subreddit)
    #     redditResults = []
    #     for post in results:
    #         redditResults.append(post.title)
    #     jsonObject = {"posts" : redditResults}

    #     return func.HttpResponse(
    #         json.dumps(jsonObject),
    #         mimetype="application/json"
    #     )

    # elif function == "getNewSubmissions":
    #     subreddit = req.params.get('subreddit')
    #     results = reddit.getNewSubmissions(subreddit)
    #     redditResults = []
    #     for post in results:
    #         redditResults.append(post.title)
    #     jsonObject = {"posts" : redditResults}

    #     return func.HttpResponse(
    #         json.dumps(jsonObject),
    #         mimetype="application/json"
    #     )

    # elif function == "getTopSubmissions":
    #     subreddit = req.params.get('subreddit')
    #     results = reddit.getTopSubmissions(subreddit)
    #     redditResults = []
    #     for post in results:
    #         redditResults.append(post.title)
    #     jsonObject = {"posts" : redditResults}

    #     return func.HttpResponse(
    #         json.dumps(jsonObject),
    #         mimetype="application/json"
    #     )

    # elif function == "parseSubmissionByTitle":
    #     return func.HttpResponse(
    #         json.dumps(jsonObject),
    #         mimetype="application/json"
    #     )

    # elif function == "parseSubmissionByBody":
    #     return func.HttpResponse(
    #         json.dumps(jsonObject),
    #         mimetype="application/json"
    #     )

    # elif function == "parseTable":
    #     return func.HttpResponse(
    #         json.dumps(jsonObject),
    #         mimetype="application/json"
    #     )

    # elif function == "parseSubmissionByUrl":
    #     return func.HttpResponse(
    #         json.dumps(jsonObject),
    #         mimetype="application/json"
    #     )  

    # elif function == "extractDealsFromSubmission":
    #     return func.HttpResponse(
    #         json.dumps(jsonObject),
    #         mimetype="application/json"
    #     )

    # elif function == "containsTable":
    #     return func.HttpResponse(
    #         json.dumps(jsonObject),
    #         mimetype="application/json"
    #     )

    # elif function == "getDeals":
    #     return func.HttpResponse(
    #         json.dumps(jsonObject),
    #         mimetype="application/json"
    #     )

    # elif function == "getSuccessRate":
    #     return func.HttpResponse(
    #         json.dumps(jsonObject),
    #         mimetype="application/json"
    #     )

    # else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
