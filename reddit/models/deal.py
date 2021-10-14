import re
import praw

def Deal():
    def __init__(submission: praw.submission):
        self.title = submission.title
        # for each title, extract certain data using Regular Expressions
        # The template is as follows: [Store Name] Deal Information (Price/percent off)
        # A full example might be: [Humble Store] Psychonauts ($1.99/80% off)
        m = re.match(r"^\[(.+?)\] (.+?) \((.+?)\)", title)
        if m is None:
            raise InvalidDealException("submission title did not match r/GameDeals format")
        else:
            self.merchant = m[1]
            self.deal = m[2]
            self.priceNpercent = m[3]
            self.m_price = re.search(r"\$\d+(\.\d+)?", priceNpercent)
            if self.m_price is None:
                raise InvalidDealException("could not derive price from submission")
            self.m_percent = re.search(r"\d+(\.\d+)?%", priceNpercent)
            if self.m_percent is None:
                raise InvalidDealException("could not derive percent off from submission")
            self.url = submission.url