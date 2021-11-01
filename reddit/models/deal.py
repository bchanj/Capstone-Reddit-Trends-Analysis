import re
import praw

class Deal:
    def __init__(self, submission: praw.models.Submission):
        self.title = submission.title
        # for each title, extract certain data using Regular Expressions
        # The template is as follows: [Store Name] Deal Information (Price/percent off)
        # A full example might be: [Humble Store] Psychonauts ($1.99/80% off)
        m = re.match(r"^\[(.+?)\] (.+?) \((.+?)\)", self.title)
        if m is None:
            raise InvalidDealException("submission title did not match r/GameDeals format")
        else:
            self.merchant = m[1]
            self.deal = m[2]
            self.priceNpercent = m[3]
            self.m_price = re.search(r"\$\d+(\.\d+)?", self.priceNpercent)
            if self.m_price is None:
                raise InvalidDealException("could not derive price from submission")
            self.m_percent = re.search(r"\d+(\.\d+)?%", self.priceNpercent)
            if self.m_percent is None:
                raise InvalidDealException("could not derive percent off from submission")
            self.url = submission.url

    # Copy deal into this deal if fields in this deal are null.
    def copyWith(self, deal: Deal) -> Deal:
        if self.title is None:
            self.title = deal.title
        if self.discount is None:
            self.discount = deal.discount
        if self.merchant is None:
            self.merchant = deal.merchant
