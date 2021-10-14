import praw
import re

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


    def getDeal():
        for submission in reddit.subreddit("GameDeals").new(limit=100):
          title = submission.title
          print('Title : ' + title)
          # for each title, extract certain data using Regular Expressions
          # The template is as follows: [Store Name] Deal Information (Price/percent off)
          # A full example might be: [Humble Store] Psychonauts ($1.99/80% off)
          m = re.match(r"^\[(.+?)\] (.+?) \((.+?)\)", title)
          if m is None:
            print("!!! TITLE DIDNOT MATCH THE EXPECTED FORMAT !!!")
          else:
            merchant = m[1]
            print('Merchant: ' + merchant)
            deal = m[2]
            print('Deal: ' + deal)
            priceNpercent = m[3]
            m_price = re.search(r"\$\d+(\.\d+)?", priceNpercent)
            if m_price is not None:
              print('Price: ' + m_price[0])
            m_percent = re.search(r"\d+(\.\d+)?%", priceNpercent)
            if m_percent is not None:
              print('Percent off: ' + m_percent[0])
            url = submission.url
            print('url: ' + url)
          print()
