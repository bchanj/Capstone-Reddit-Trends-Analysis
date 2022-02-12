import datetime
from typing import List
from deal import Deal, GameDeal, DictionaryKeys

class Bundle:
    """Represents a bundle and contains deals.

    Unit Tests:
    >>> g = GameDeal(title="Awesome Sale")
    >>> g.setAttribute("Sale", "80%")
    >>> g.discount == "80%"
    True
    >>> b = Bundle()
    >>> b.deals.append(g)
    >>> b.deals
    [Awesome Sale]
    """
    def __init__(self,
                 id: str="",
                 subreddit: str="r/GameDeals",
                 title: str="",
                 merchant: str="",
                 discount: str="",
                 url: str="",
                 date: str=datetime.datetime.now().strftime("%m-%d-%Y"),
                 deals: List[Deal]=[]):
        self.id=id
        self.subreddit=subreddit
        self.title=title
        self.merchant=merchant
        self.discount=discount
        self.url=url
        self.deals=deals

    def getCosmosDBObject(self) -> dict:
        """Cosmos DB API expects dictionaries.

        Unit Tests:
        >>> d1 = Deal()
        >>> d1.title = "My Title"
        >>> d1.price = "$55"
        >>> d1.discount = "20%"
        >>> d2 = Deal()
        >>> d2.title = "ThisIsAVeryLongTitle"
        >>> d2.price_eur = "€20"
        >>> d2.discount = "60%"
        >>> b = Bundle()
        >>> b.id = "abc123"
        >>> b.date = "1-30-2022"
        >>> b.merchant = "barancompany"
        >>> b.title = "barangame"
        >>> b.subreddit = "breddit"
        >>> b.url = "barangames.com"
        >>> b.discount = "up to 50%"
        >>> b.deals = [d1, d2]
        >>> b.getCosmosDBObject()
        {'id': 'abc123', 'date': '1-30-2022', 'merchant': 'barancompany', 'title': 'barangame', 'subreddit': 'breddit', 'url': 'barangames.com', 'discount': 'up to 50%', 'deals': [{'title': 'My Title', 'discount': '20%', 'usd': '$55'}, {'title': 'ThisIsAVeryLongTitle', 'discount': '60%', 'eur': '€20'}]}
        """
        myDict = {}
        if self.id != '':
            myDict[DictionaryKeys.ID.value] = self.id
        if self.date != '':
            myDict[DictionaryKeys.DATE.value] = self.date
        if self.merchant != '':
            myDict[DictionaryKeys.MERCHANT.value] = self.merchant
        if self.title != '':
            myDict[DictionaryKeys.TITLE.value] = self.title
        if self.subreddit != '':
            myDict[DictionaryKeys.SUBREDDIT.value] = self.subreddit
        if self.url != '':
            myDict[DictionaryKeys.URL.value] = self.url
        if self.discount != '':
            myDict[DictionaryKeys.DISCOUNT.value] = self.discount
        dealsList = []
        for deal in self.deals:
            dealDict = deal.getCosmosDBObject()
            dealsList.append(dealDict)
        myDict[DictionaryKeys.DEALS.value] = dealsList
        return myDict

if __name__ == "__main__":
    import doctest
    doctest.testmod()