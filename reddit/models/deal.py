import re
import praw
import datetime

from typing import Dict

class Deal:
    def __init__(self, subreddit: str="", title: str="", merchant: str="", discount: str="", price: str="", date: str=datetime.datetime.now().strftime("%m-%d-%Y"), synonyms: Dict[str, str]={}):
        self.subreddit = subreddit
        self.title = title
        self.discount = discount
        self.merchant = merchant
        self.date = date
        self.price = price
        self.synonyms = synonyms

    def isValid(self) -> bool:
        """Returns True if deal contains:
        1. title
        2. discount or price

        Returns:
            bool: True if deal contains required fields else False

        Unit Tests:
        >>> d = Deal(subreddit="r/GameDeals", title="ABC", discount="ABC")
        >>> d.isValid()
        True
        >>> d = Deal(subreddit="r/GameDeals", title="ABC", price="ABC")
        >>> d.isValid()
        True
        >>> d = Deal(merchant="ABC")
        >>> d.isValid()
        False
        """
        return self.title != "" and self.subreddit != "" and ( self.discount != "" or self.price != "" ) 

    def setAttribute(self, synonym: str, value: str) -> None:
        """Set class attribute with regular expression matching.
        Uses self.synonym: Dict to match attribute names.
        Upon successful match, will parse the value

        Args:
            synonym (str): Synonym to match with an atrribute
            value (str): value to set the attribute with

        Unit Tests:
        >>> d = Deal(synonyms={"title": [r"^[G|g]ame$"], "discount": [r"^[S|s]ale$"],"price": [r"^[U|u][S|s][D|d]$"],})
        >>> d.setAttribute("404NotFound", 0)
        >>> d.title == ""
        True
        >>> d.discount == ""
        True
        >>> d.price == ""
        True
        >>> d.merchant == ""
        True
        >>> d.setAttribute("Sale", "80%")
        >>> d.discount == "80%"
        True
        >>> d.setAttribute("game", "Halo Infinite")
        >>> d.title == "Halo Infinite"
        True
        >>> d.setAttribute("USD", "$99")
        >>> d.price == "$99"
        True
        """
        for attribute, synonym_list in self.synonyms.items():
            if any([ re.compile(regex).match(synonym) for regex in synonym_list ]):
                setattr(self, attribute, value)
                break


class GameDeal(Deal):
    """Deal child class representing game deals.
    Purpose: provide a synonym dictionary to set deal attributes

    Args:
        Deal ([type]): Super class -> Do not remove
    
    Unit Tests:
    >>> g = GameDeal()
    >>> g.setAttribute("Sale", "80%")
    >>> g.discount == "80%"
    True
    >>> g.setAttribute("game", "Halo Infinite")
    >>> g.title == "Halo Infinite"
    True
    >>> g.setAttribute("USD", "$99")
    >>> g.price == "$99"
    True
    """
    def __init__(self, title: str="", merchant: str="", discount: str="", date: str=datetime.datetime.now().strftime("%m-%d-%Y"), price: str=""):
        super().__init__(
            subreddit='r/GameDeals',
            title=title, 
            merchant=merchant, 
            discount=discount, 
            price=price, 
            synonyms={
            "title": [
                r"^[G|g]ame$"],
            "discount": [
                r"^[S|s]ale$"],
            "price": [
                r"^[U|u][S|s][D|d]$"],})

if __name__ == "__main__":
    import doctest
    doctest.testmod()
