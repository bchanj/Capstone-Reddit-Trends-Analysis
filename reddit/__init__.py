from cgi import test
import http
from importlib.resources import path
import logging
import os
import sys
import glob
import json
from unittest import result
import azure.functions as func
from pathlib import Path
from os.path import exists
sys.path.append(os.path.dirname(__file__))
from models import reddit_client

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    function = req.params.get('function')
    jsonObject = {}
    if not function:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            function = req_body.get('function')

    if function == "getHotSubmissions":
        reddit = reddit_client.RedditClient()
        subreddit = req.params.get('subreddit')
        results = reddit.getNewSubmissions(subreddit)
        redditResults = []
        for post in results:
            redditResults.append(post.title)
        jsonObject = {"posts" : redditResults}

        return func.HttpResponse(
            json.dumps(jsonObject),
            mimetype="application/json"
        )

    elif function == "getNewSubmissions":
        reddit = reddit_client.RedditClient()
        subreddit = req.params.get('subreddit')
        results = reddit.getNewSubmissions(subreddit)
        redditResults = []
        for post in results:
            redditResults.append(post.title)
        jsonObject = {"posts" : redditResults}

        return func.HttpResponse(
            json.dumps(jsonObject),
            mimetype="application/json"
        )

    elif function == "getTopSubmissions":
        reddit = reddit_client.RedditClient()
        subreddit = req.params.get('subreddit')
        results = reddit.getTopSubmissions(subreddit)
        redditResults = []
        for post in results:
            redditResults.append(post.title)
        jsonObject = {"posts" : redditResults}

        return func.HttpResponse(
            json.dumps(jsonObject),
            mimetype="application/json"
        )

    elif function == "parseSubmissionByTitle":
        return func.HttpResponse(
            json.dumps(jsonObject),
            mimetype="application/json"
        )

    elif function == "parseSubmissionByBody":
        return func.HttpResponse(
            json.dumps(jsonObject),
            mimetype="application/json"
        )

    elif function == "parseTable":
        return func.HttpResponse(
            json.dumps(jsonObject),
            mimetype="application/json"
        )

    elif function == "parseSubmissionByUrl":
        return func.HttpResponse(
            json.dumps(jsonObject),
            mimetype="application/json"
        )  

    elif function == "extractDealsFromSubmission":
        return func.HttpResponse(
            json.dumps(jsonObject),
            mimetype="application/json"
        )

    elif function == "containsTable":
        return func.HttpResponse(
            json.dumps(jsonObject),
            mimetype="application/json"
        )

    elif function == "getDeals":
        return func.HttpResponse(
            json.dumps(jsonObject),
            mimetype="application/json"
        )

    elif function == "getSuccessRate":
        return func.HttpResponse(
            json.dumps(jsonObject),
            mimetype="application/json"
        )

    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
