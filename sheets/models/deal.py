from typing import List

class Deal():
    def __init__(self, date: str, title: str):
        self.date = None
        self.title = None
        
    # get all named attributes for this object as a list of str
    def getAttributes() -> List[str]:
        [attr for attr in c.__dict__.keys() if attr[:1] != '_']