import datetime
import logging
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
from reddit_client import RedditClient, SubredditTarget, SubredditFeedFilter
from typing import List
from deal import Deal
import azure.functions as func
import glob
import http
import json
import logging

import azure.functions as func
    
def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    client = RedditClient()
    deals: List[Deal] = client.getDeals(
      subreddit_target=SubredditTarget.GAMEDEALS, 
      subreddit_type=SubredditFeedFilter.NEW,
      limit=100,
    )
    cosmos = CosmosClientWrapper()
    cosmos.createEntries(deals)
    logging.info('Python timer trigger function ran at %s', utc_timestamp)

