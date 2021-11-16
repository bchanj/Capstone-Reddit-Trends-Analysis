import re
import praw

class Deal:
    def __init__(self):
        self.title = None
        self.discount = None
        self.merchant = None
        self.containsTable = None