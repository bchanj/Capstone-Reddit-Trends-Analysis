import re
import praw
import datetime
import json
from enum import Enum
from typing import List,Dict

# We turn our objects into dictionaries before we push to Cosmos DB.
# These are the keys that we use in these dictionaries.
class DictionaryKeys(Enum):
  TITLE = "title"
  BUNDLE_TITLE = "bundle_title"
  MERCHANT = "merchant"
  DISCOUNT = "discount"
  PRICE = "usd"
  PRICE_EUR = "eur"
  PRICE_GBP = "gbp"
  DATE = "date"
  ID = "id"
  BUNDLE_ID = "bundle_id"
  URL = "url"
  SUBREDDIT = "subreddit"
  DEALS = "deals"

class Deal:
    def __init__(self,
                 subreddit: str="",
                 url: str="",
                 bundle_id: str="",
                 bundle_title: str="",
                 date: str=datetime.datetime.now().strftime("%m-%d-%Y"),
                 merchant: str="",
                 id: str="",
                 title: str="",
                 discount: str="",
                 price: str="",
                 price_eur: str="",
                 price_gbp: str="",
                 synonyms: Dict[str, str]={}):
        self.subreddit = subreddit
        self.url = url
        self.bundle_id = bundle_id
        self.bundle_title = bundle_title
        self.date = date
        self.merchant = merchant
        self.id = id
        self.title = title
        self.discount = discount
        self.price = price
        self.price_eur = price_eur
        self.price_gbp = price_gbp
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
        False
        >>> d = Deal(id="abc1", subreddit="r/GameDeals", title="ABC", price="ABC")
        >>> d.isValid()
        False
        >>> d = Deal(bundle_id="abc", subreddit="r/GameDeals", title="ABC", price_eur="ABC")
        >>> d.isValid()
        False
        >>> d = Deal(id="abc1", bundle_id="abc", subreddit="r/GameDeals", title="ABC", discount="ABC")
        >>> d.isValid()
        True
        >>> d = Deal(id="abc1", bundle_id="abc", subreddit="r/GameDeals", title="ABC", price="ABC")
        >>> d.isValid()
        True
        >>> d = Deal(id="abc1", bundle_id="abc", subreddit="r/GameDeals", title="ABC", price_eur="ABC")
        >>> d.isValid()
        True
        >>> d = Deal(id="abc1", bundle_id="abc", merchant="ABC")
        >>> d.isValid()
        False
        """
        return (self.id != ""
          and self.bundle_id != ""
          and self.title != ""
          and self.subreddit != ""
          and ( self.discount != "" or self.price != "" or self.price_eur != "" or self.price_gbp != ""))

    def setAttribute(self, synonym: str, value: str) -> None:
        """Set class attribute with regular expression matching.
        Uses self.synonym: Dict to match attribute names.
        Upon successful match, will parse the value

        Args:
            synonym (str): Synonym to match with an atrribute
            value (str): value to set the attribute with

        Unit Tests:
        >>> d = Deal(synonyms={"title": [r"^[G|g][A|a][M|m][E|e]$"], "discount": [r"^[S|s]ale$"],"price": [r"^[U|u][S|s][D|d]$", r"^[P|p][R|r][I|i][C|c][E|e]$"],"price_eur": [r"^[E|e][U|u][R|r].*"],"price_gbp": [r"^[G|g][B|b][P|p]$", r"^[P|p][O|o][U|u][N|n][D|d]$"],})
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
        >>> d.setAttribute("Price", "$199")
        >>> d.price == "$199"
        True
        >>> d.setAttribute("Eur", "€99")
        >>> d.price_eur == "€99"
        True
        >>> d.setAttribute("GBP", "£99")
        >>> d.price_gbp == "£99"
        True
        """
        for attribute, synonym_list in self.synonyms.items():
            if any([ re.compile(regex).match(synonym) for regex in synonym_list ]):
                setattr(self, attribute, value)
                break

    def getCosmosDBObject(self) -> dict:
        """Cosmos DB API expects dictionaries.

        Unit Tests:
        >>> d1 = Deal()
        >>> d1.bundle_id = "abc"
        >>> d1.id = "abc1"
        >>> d1.date = "1-30-2022"
        >>> d1.merchant = "barancompany"
        >>> d1.bundle_title = "baransgames"
        >>> d1.subreddit = "breddit"
        >>> d1.url = "barangames.com"
        >>> d1.title = "My Title"
        >>> d1.price = "$55"
        >>> d1.discount = "20%"
        >>> d1.getCosmosDBObject()
        {'subreddit': 'breddit', 'url': 'barangames.com', 'bundle_id': 'abc', 'bundle_title': 'baransgames', 'date': '1-30-2022', 'merchant': 'barancompany', 'id': 'abc1', 'title': 'My Title', 'discount': '20%', 'usd': '$55'}

        >>> d2 = Deal()
        >>> d2.bundle_id = "abc"
        >>> d2.id = "abc2"
        >>> d2.title = "ThisIsAVeryLongTitle"
        >>> d2.price_eur = "€20"
        >>> d2.discount = "60%"
        >>> d2.getCosmosDBObject()
        {'bundle_id': 'abc', 'date': '02-21-2022', 'id': 'abc2', 'title': 'ThisIsAVeryLongTitle', 'discount': '60%', 'eur': '€20'}
        """
        myDict = {}
        if self.subreddit != '':
            myDict[DictionaryKeys.SUBREDDIT.value] = self.subreddit
        if self.url != '':
            myDict[DictionaryKeys.URL.value] = self.url
        if self.bundle_id != '':
            myDict[DictionaryKeys.BUNDLE_ID.value] = self.bundle_id
        if self.bundle_title != '':
            myDict[DictionaryKeys.BUNDLE_TITLE.value] = self.bundle_title
        if self.date != '':
            myDict[DictionaryKeys.DATE.value] = self.date
        if self.merchant != '':
            myDict[DictionaryKeys.MERCHANT.value] = self.merchant
        if self.id != '':
            myDict[DictionaryKeys.ID.value] = self.id
        if self.title != '':
            myDict[DictionaryKeys.TITLE.value] = self.title
        if self.discount != '':
            myDict[DictionaryKeys.DISCOUNT.value] = self.discount
        if self.price != '':
            myDict[DictionaryKeys.PRICE.value] = self.price
        if self.price_eur != '':
            myDict[DictionaryKeys.PRICE_EUR.value] = self.price_eur
        if self.price_gbp != '':
            myDict[DictionaryKeys.PRICE_GBP.value] = self.price_gbp
        return myDict

    # Override of str method of our deal object.
    def __iter__(self):
        yield from self.__dict__.items()
    
    def __str__(self):
        return json.dumps({x: dict(self)[x] for x in dict(self) if x not in ["synonyms"]}, ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

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
    >>> g.setAttribute("off", "20%")
    >>> g.discount == "20%"
    True
    >>> g.setAttribute("%", "70%")
    >>> g.discount == "70%"
    True
    >>> g.setAttribute("game", "Halo Infinite")
    >>> g.title == "Halo Infinite"
    True
    >>> g.setAttribute("US ($)", "$99")
    >>> g.price == "$99"
    True
    >>> g.setAttribute("Product Price (USD)", "$199")
    >>> g.price == "$199"
    True
    >>> g.setAttribute("Pound", "£99")
    >>> g.price_gbp == "£99"
    True
    >>> g.setAttribute("Euro", "€99")
    >>> g.price_eur == "€99"
    True
    >>> d = GameDeal(price_eur= "€99")
    >>> g.price_eur
    '€99'
    """
    def __init__(self,
                 url: str="",
                 bundle_id: str="",
                 bundle_title: str="",
                 date: str=datetime.datetime.now().strftime("%m-%d-%Y"),
                 merchant: str="",
                 id: str="",
                 title: str="",
                 discount: str="",
                 price: str="",
                 price_eur: str="",
                 price_gbp: str=""):
        super().__init__(
            subreddit = 'r/GameDeals',
            url = url,
            bundle_id = bundle_id,
            bundle_title = bundle_title,
            date = date,
            merchant = merchant,
            id = id,
            title = title,
            discount = discount,
            price = price,
            price_eur = price_eur,
            price_gbp = price_gbp,
            synonyms = {
            "title": [
                r".*[D|d][E|e][A|a][L|l].*",
                r".*[G|g][A|a][M|m][E|e].*",
                r".*[T|t][I|i][T|t][L|l][E|e].*"],
            "discount": [
                r".*%.*",
                r".*[S|s][A|a][L|l][E|e].*",
                r".*[D|d][I|i][S|s][C|c].*",
                r".*[O|o][F|f][F|f].*"],
            "price": [
                r".*[U|u][S|s][D|d].*",
                r".*\$.*",
                r".*[P|p][R|r][I|i][C|c][E|e].*"],
            "price_eur": [
                r".*€.*",
                r".*[E|e][U|u][R|r].*"],
            "price_gbp": [
                r".*£.*",
                r".*[G|g][B|b][P|p].*",
                r".*[P|p][O|o][U|u][N|n][D|d].*"]})
        
    def __iter__(self):
        yield from self.__dict__.items()
    
    def __str__(self):
        return json.dumps({x: dict(self)[x] for x in dict(self) if x not in ["synonyms"]}, ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
