import praw
from enum import Enum

class Subreddit_Type(Enum):
    RELEVANCE = "relevance",
    HOT = "hot",
    TOP = "top",
    NEW = "new",
    COMMENTS = "comments"

class reddit_client:
    """
    DOCSTRING
    """
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id="5J0BbjbzNZrNzSnZNOwCOQ",
            client_secret="JWno2YEOiAOhnY0tZDVtjGa6TWolTQ",
            password="ZhXEUe*k3qV2Ukf*vj3wuogD",
            user_agent="testscript",
            username="North-Alternative886",
        )
        self.reddit.read_only = True # change if editing