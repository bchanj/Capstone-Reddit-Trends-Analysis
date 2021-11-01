import re
import praw

class Deal:
    def __init__(self):
        self.title = None
        self.discount = None
        self.merchant = None

    # Copy deal into this deal if fields in this deal are null.
    def copyWith(self, deal: Deal) -> None:
        if self.title is None:
            self.title = deal.title
        if self.discount is None:
            self.discount = deal.discount
        if self.merchant is None:
            self.merchant = deal.merchant
