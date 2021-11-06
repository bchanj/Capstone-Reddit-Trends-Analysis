import praw
import re
from enum import Enum
from typing import List
from reddit.models.deal import Deal

class InvalidDealException(Exception):
  def __init__(message: str):
    self.message = message
    super().__init__(self.message)

class SubredditType(Enum):
  HOT = "hot"
  NEW = "new"
  TOP = "top"


class reddit_client:
    """
    DOCSTRING
    """
    def __init__(self):
      self.DEFAULT_LIMIT=100
      self.reddit = praw.Reddit(
          client_id="5J0BbjbzNZrNzSnZNOwCOQ",
          client_secret="JWno2YEOiAOhnY0tZDVtjGa6TWolTQ",
          password="ZhXEUe*k3qV2Ukf*vj3wuogD",
          user_agent="testscript",
          username="North-Alternative886",
      )

      self.reddit.read_only = True # change if editing

      self.subreddit_function_table = {
        SubredditType.HOT: self.getHotSubmissions,
        SubredditType.NEW: self.getNewSubmissions,
        SubredditType.TOP: self.getTopSubmissions,
      }

    def getHotSubmissions(self, subreddit_title: str, limit:int=None):
      if limit is None:
        limit = self.DEFAULT_LIMIT
      return self.reddit.subreddit(subreddit_title).hot(limit=limit)

    def getNewSubmissions(self, subreddit_title: str, limit:int=None):
      if limit is None:
        limit = self.DEFAULT_LIMIT
      return self.reddit.subreddit(subreddit_title).new(limit=limit)

    def getTopSubmissions(self, subreddit_title: str, limit:int=None):
      if limit is None:
        limit = self.DEFAULT_LIMIT
      return self.reddit.subreddit(subreddit_title).top(limit=limit)

    def find_data(self, name):
        gd = self.reddit.subreddit(name)
        for submission in gd.hot(limit=5):
            print(submission.title)

    def getDeals(self, subreddit_title: str, subreddit_type: SubredditType, limit:int = 1000) -> List[Deal]:
      deals = []
      for submission in self.subreddit_function_table[subreddit_type](subreddit_title, limit):
        try:
          # attempt to construct deal with the submission
          Deal(submission)
        except Exception as e:
          # if the deal does not construct successfully continue
          continue
        deals += [Deal(submission)]
      return deals


    def getSuccessRate(self, subreddit_title: str):
      sample_size: int = 10000
      for subreddit_type in SubredditType:
        successfully_parsed_deals = [deal for deal in self.subreddit_function_table[subreddit_type](subreddit_title, sample_size)]
        print(str(subreddit_type) + ": " + str(len(successfully_parsed_deals)/sample_size*100) + "%")


    #DELETE
    def PostByID(self, id):
        return self.reddit.submission(id).title