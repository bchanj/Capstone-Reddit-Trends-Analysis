import praw
import re

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


    def getDeal(subreddit_title: str, limit:int = 100):
        for submission in reddit.subreddit(subreddit_title).new(limit):
          title = submission.title
          # for each title, extract certain data using Regular Expressions
          # The template is as follows: [Store Name] Deal Information (Price/percent off)
          # A full example might be: [Humble Store] Psychonauts ($1.99/80% off)
          m = re.match(r"^\[(.+?)\] (.+?) \((.+?)\)", title)
          if m is None:
            raise InvalidDealException("submission title did not match r/GameDeals format")
          else:
            merchant = m[1]
            deal = m[2]
            priceNpercent = m[3]
            m_price = re.search(r"\$\d+(\.\d+)?", priceNpercent)
            if m_price is None:
              raise InvalidDealException("could not derive price from submission")
            m_percent = re.search(r"\d+(\.\d+)?%", priceNpercent)
            if m_percent is None:
              raise InvalidDealException("could not derive percent off from submission")
            url = submission.url
