import praw
import re
import bs4 
from enum import Enum
from typing import List, Dict
from deal import Deal, GameDeal

class SubredditFeedFilter(Enum):
  HOT = "hot"
  NEW = "new"
  TOP = "top"

class SubredditTarget(Enum):
  GAMEDEALS = "GameDeals"
  MUA = "MUAonTheCheap"

class RedditClient:
    """
    DOCSTRING
    """
    def __init__(self):
      super().__init__()
      self.DEFAULT_LIMIT=100
      self.reddit = praw.Reddit(
          client_id="5J0BbjbzNZrNzSnZNOwCOQ",
          client_secret="JWno2YEOiAOhnY0tZDVtjGa6TWolTQ",
          password="ZhXEUe*k3qV2Ukf*vj3wuogD",
          user_agent="testscript",
          username="North-Alternative886",
      )

      self.reddit.read_only = True # change if editing

      # Map of subreddit types to PRAW function for scraping
      self.subreddit_function_table: Dict[reddit.reddit_client.SubredditFeedFilter, function] = {
        SubredditFeedFilter.HOT: self.getHotSubmissions,
        SubredditFeedFilter.NEW: self.getNewSubmissions,
        SubredditFeedFilter.TOP: self.getTopSubmissions,
      }
      
      # Map subreddit name to rules defined by that subreddit
      self.subreddit_rules: Dict[SubredditTarget, str] = {
        SubredditTarget.GAMEDEALS: r"^\[(?P<merchant>.+?)\] (?P<title>.+?) \((?P<discount>.+?)\)",
      }

      self.subreddit_deal_constructors = {
        SubredditTarget.GAMEDEALS: GameDeal
      }

    def getHotSubmissions(self, subreddit_title: str, limit:int=None):
      if limit is None:
        limit = self.DEFAULT_LIMIT
      return self.reddit.subreddit(subreddit_title).hot(limit=limit)

    def getNewSubmissions(self, subreddit_title: str, limit:int=None):
      if limit is None:
        limit = self.DEFAULT_LIMIT
      return self.reddit.subreddit(subreddit_title).new(limit=limit)

    def getTopSubmissions(self, subreddit_title: str, limit:int=None):
      if limit is None:
        limit = self.DEFAULT_LIMIT
      return self.reddit.subreddit(subreddit_title).top(limit=limit)

    # try to parse deal by title based on subreddit rules
    # before calling for new subreddit, create new entry in subreddit_rules Map with 
    # with a new SubredditTarget to string (Regex Rules) 
    # RAISES DoesNotFollowRulesException if unsuccessful
    def parseSubmissionByTitle(self, 
                              subreddit_target: SubredditTarget, 
                              submission: praw.models.Submission) -> Deal:
      """[summary]

      Args:
          subreddit_target (SubredditTarget): [description]
          submission (praw.models.Submission): [description]

      Raises:
          DoesNotFollowRulesException: [description]

      Returns:
          Deal: [description]

      unit tests:
          >>> 

      """
      deal: Deal = Deal()
      m = re.match(self.subreddit_rules[subreddit_target], submission.title)
      if m is None:
        raise DoesNotFollowRulesException()
      else:
          deal.merchant = m.group("merchant")
          deal.title = m.group("title")
          deal.discount = m.group("discount")
          deal.url = submission.url
      return deal

    def parseTitle(self, title_text: str, subreddit_target: SubredditTarget) -> List[Deal]:
      """[summary]
      Args:
          title_text (str): [description]
          subreddit_target (SubredditTarget): [description]

      Returns:
          List[Deal]: [description]

      unit tests:
          >>> client = RedditClient()
          >>> title = "[Gamesplanet] Ghosts 'n Goblins Resurrection (50%)" 
          >>> deals = client.parseTitle(title, SubredditTarget.GAMEDEALS)
          >>> len(deals) == 1
          True
          >>> title = "[Gamesplanet] Ghosts 'n Goblins Resurrection (50%), Beyond Good & Evil (70%), UNO (60%)" 
          >>> deals = client.parseTitle(title, SubredditTarget.GAMEDEALS)
          >>> len(deals) == 3
          True
          >>> title = "[Gamesplanet] Ghosts 'n Goblins Resurrection (-50%)" 
          >>> deals = client.parseTitle(title, SubredditTarget.GAMEDEALS)
          >>> len(deals) == 1
          True
          >>> title = "[Gamesplanet] Weekly Deals: Ghosts 'n Goblins Resurrection (-50%), Beyond Good & Evil (-70%), UNO (-60%), Rayman Legends (-75%), Ultimate Marvel vs. Capcom 3 (-76%), Prince of Persia (-80%), Devil May Cry 5 Deluxe + Vergil (-41%), Disney Afternoon Collection (-80%)" 
          >>> deals = client.parseTitle(title, SubredditTarget.GAMEDEALS)
          >>> len(deals) == 8
          True
          >>> title = "[GMG] Tennis Manager 2021 (£14.00| €16.00 | $16.00 / 60%)" 
          >>> deals = client.parseTitle(title, SubredditTarget.GAMEDEALS)
          >>> len(deals) == 1
          True
          >>> title = "[GOG] The Darkside Detective (Win/Mac/Linux) (£3.19 / -68% off)" 
          >>> deals = client.parseTitle(title, SubredditTarget.GAMEDEALS)
          >>> len(deals) == 1
          True
          >>> title = "[GamersGate] THQ Nordic Sale: Quantum Break (-75% | $8.89 / €8.22 / £6.66 w/ code); Sunset Overdrive (-25% | $13.34 / €13.34 / £10.00 w/ code) | Steam | Use code RGAMEDEALS to save 11%" 
          >>> deals = client.parseTitle(title, SubredditTarget.GAMEDEALS)
          >>> len(deals) == 2
          True
      """
      dealList = re.split('; |, ', title_text)
      # Find the retailer and append it to the beginning of each additional deal (any past the first entry)

      return dealList


    def parseSubmissionByBody(self, submission: praw.models.Submission, subreddit_target: SubredditTarget) -> List[Deal]:
      """Looks for a table in praw.models.submission.selftext_html (body) and attempts to
      parse a list of deals.

      Args:
          submission (praw.models.Submission): A Submission object as defined by the PRAW API

      Returns:
          List[Deal]: A list of deals that are successfully parsed.
      """
      return parseTable(self, html=submission.selftext_html, subreddit_target=subreddit_target)
      
    def parseTable(self, html: str, subreddit_target: SubredditTarget) -> List[Deal]:
      """Scans a HTML table and parses it for a list of deals 

      Args:
          html (str): string of HTML parsable with bs4

      Returns:
          List[Deal]: a list of successfully parsed Deals

      Unit Tests: 
        >>> client = RedditClient()
        >>> html = '<table class="MRH-njmSb5ZTkfb1o4dqv"><thead><tr class="s6JZe6869f81l9E_5G7Q9"><th class="_3TNkDptlyGOiWXvdX_acOB">Game</th><th class="_3TNkDptlyGOiWXvdX_acOB">Sale</th><th class="_3TNkDptlyGOiWXvdX_acOB">USD</th></tr></thead><tbody><tr class="s6JZe6869f81l9E_5G7Q9"><td class="_3DYfYn_cczg1wj_a3hhyV6">Dungeon of the Endless - Definitive Edition</td><td class="_3DYfYn_cczg1wj_a3hhyV6">80%</td><td class="_3DYfYn_cczg1wj_a3hhyV6">$3.99</td></tr><tr class="s6JZe6869f81l9E_5G7Q9"><td class="_3DYfYn_cczg1wj_a3hhyV6">Endless Legend - Monstrous Tales</td><td class="_3DYfYn_cczg1wj_a3hhyV6">33%</td><td class="_3DYfYn_cczg1wj_a3hhyV6">$2.00</td></tr></tbody></table>'
        >>> deals = client.parseTable(html=html, subreddit_target=SubredditTarget.GAMEDEALS)
        >>> len(deals) == 2
        True
        >>> html = '<table class="MRH-njmSb5ZTkfb1o4dqv"><thead><tr class="s6JZe6869f81l9E_5G7Q9"><th class="_3TNkDptlyGOiWXvdX_acOB">UNKNOWN</th><th class="_3TNkDptlyGOiWXvdX_acOB">Sale</th><th class="_3TNkDptlyGOiWXvdX_acOB">USD</th></tr></thead><tbody><tr class="s6JZe6869f81l9E_5G7Q9"><td class="_3DYfYn_cczg1wj_a3hhyV6">Dungeon of the Endless - Definitive Edition</td><td class="_3DYfYn_cczg1wj_a3hhyV6">80%</td><td class="_3DYfYn_cczg1wj_a3hhyV6">$3.99</td></tr><tr class="s6JZe6869f81l9E_5G7Q9"><td class="_3DYfYn_cczg1wj_a3hhyV6">Endless Legend - Monstrous Tales</td><td class="_3DYfYn_cczg1wj_a3hhyV6">33%</td><td class="_3DYfYn_cczg1wj_a3hhyV6">$2.00</td></tr></tbody></table>'
        >>> deals = client.parseTable(html=html, subreddit_target=SubredditTarget.GAMEDEALS)
        >>> len(deals) == 0
        True
        >>>
      """
      deals: List[Deal] = [] # result from parsing all tables
      soup = bs4.BeautifulSoup(html, features="html.parser")
      tables = soup.findAll('table')
      for table in tables:
        headers = [ header.text for header in table.findAll('th')]
        tvalues = [[ cell.text for cell in row.findAll('td')] for row in table.findAll('tr')][1:]
        for row in tvalues:
          deal: Deal = self.subreddit_deal_constructors[subreddit_target]()
          for index, value in enumerate(row):
            # Use the table headers to look up Deal attribute with synonyms
            deal.setAttribute(headers[index], value)
          if deal.isValid():
            deals.append(deal)
      return deals

    def parseSubmissionByUrl(self, submission:praw.models.Submission) -> List[Deal]:
      deals: List[Deal] = []
      return deals

    def extractDealsFromSubmission(self, 
                                  subreddit_target: SubredditTarget, 
                                  submission: praw.models.Submission) -> List[Deal]:
      deals: List[Deal] = []
      # attempt to parse the submission by title
      if self.containsTable(submission):
        # attempt to parse the submission body 
        # look for tables while we are at it
        try:
          results: List[Deal] = self.parseSubmissionByBody(submission)
          deals.append(results)
        except:
          pass
      else:
        try:
          results: List[Deal] = self.parseSubmissionByTitle(subreddit_target, submission) # raises DoesNotFollowRulesException 
          deals.append(results)
        except DoesNotFollowRulesException:
          # If we are not successful in parsing by title then we can write to logs
          pass

      return deals

    def containsTable(self, submission: praw.models.Submission) -> bool:
      for line in submission.selftext.split('\n'):
        if re.match(r"(-|:|\|)+", line):
          return True
      return False

    def getDeals(self, 
                # Needs a target to scrape
                subreddit_target: SubredditTarget, 
                # Default to new posts if no override.
                subreddit_type: SubredditFeedFilter = SubredditFeedFilter.NEW, 
                # Default to 1000 posts if no override.
                limit:int = 1000) -> List[Deal]:
      deals: List[Deal] = []
      # Gets posts from subreddit_target filtered by subreddit_type limited to limit number of posts.
      for submission in self.subreddit_function_table[subreddit_type](subreddit_target.value, limit):
        deals.append(self.extractDealsFromSubmission(subreddit_target, submission))
      return deals


    def getSuccessRate(self, subreddit_title: str):
      sample_size: int = 10000
      for subreddit_type in SubredditFeedFilter:
        successfully_parsed_deals = [deal for deal in self.subreddit_function_table[subreddit_type](subreddit_title, sample_size)]
        print(str(subreddit_type) + ": " + str(len(successfully_parsed_deals)/sample_size*100) + "%")

    # def _flatten(self, arr: List) -> List:
    #   return [element for subarr in arr for element in subarr]

if __name__ == "__main__":
    import doctest
    doctest.testmod()