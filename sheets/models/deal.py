import datetime
from typing import List

class Deal():
    def __init__(self, 
        # subreddit is a required parameter
        subreddit: str, 
        title: str, 
        date: str=datetime.datetime.now().strftime("%m-%d-%Y")):
        if subreddit == None or not subreddit.strip():
            raise Exception("Deal objects must have a subreddit")
        self.subreddit = subreddit

        # default to datetime now if no date is provided
        self.date = datetime.datetime.now().strftime("%m-%d-%Y") if date is None else date
        
        self.title = title
        
    # get all named attributes for this object as a list of str
    def getAttributes() -> List[str]:
        [attr for attr in c.__dict__.keys() if attr[:1] != '_']