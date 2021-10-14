import praw
import re
from typing import List

# from reddit.models.deal import Deal

class InvalidDealException(Exception):
  def __init__(message: str):
    self.message = message
    super().__init__(self.message)


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

    def find_data(self, name):
        gd = self.reddit.subreddit(name)
        for submission in gd.hot(limit=5):
            print(submission.title)


    def getDeals(self, subreddit_title: str, limit:int = 1000) -> List[Deal]:
      deals = []
      for submission in self.reddit.subreddit(subreddit_title).new(limit=limit):
        try:
          # attempt to construct deal with the submission
          Deal(submission)
        except Exception as e:
          # if the deal does not construct successfully continue
          continue
        deals += [Deal(submission)]
      return deals

    def getSuccessRate(self):
      sample_size: int = 10000
      successfully_parsed_deals = self.getDeals("GameDeals", sample_size)
      return len(successfully_parsed_deals)/sample_size

