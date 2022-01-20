import praw
import re
import bs4 
from enum import Enum
from typing import List, Dict
from deal import Deal

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

    def parseSubmissionByBody(self, submission: praw.models.Submission) -> List[Deal]:
      """Looks for a table in praw.models.submission.selftext_html (body) and attempts to
      parse a list of deals.

      Args:
          submission (praw.models.Submission): A Submission object as defined by the PRAW API

      Returns:
          List[Deal]: A list of deals that are successfully parsed.
      """
      deals: List[Deal] = [] # result from parsing all tables
      soup = bs4.BeautifulSoup(submission.selftext_html, features="html.parser")
      tables = soup.findAll('table')
      for table in tables:
        headers = [ header.text for header in table.findAll('th')]
        tvalues = [[ cell.text for cell in row.findAll('td')] for row in table.findAll('tr')][1:]
        
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
