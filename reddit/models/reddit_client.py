#!/usr/bin/env python3
import sys
import os
import praw
import re
import bs4
import datetime
from enum import Enum
from typing import List, Dict

sys.path.append(os.path.dirname(__file__))
from deal import Deal, GameDeal, Bundle
from exceptions import DoesNotFollowRulesException


class SubredditFeedFilter(Enum):
  TOP = "top"
  NEW = "new"
  HOT = "hot"

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
                              submission: praw.models.Submission) -> Bundle:
      bundle = self.parseTitle(submission.title)
      bundle.subreddit = subreddit_target
      bundle.url = submission.url
      bundle.date = datetime.datetime.fromtimestamp(submission.created).strftime("%m-%d-%Y")
      bundle.id = submission.id
      return bundle
    
    def parseTitle(self, title) -> Bundle:
      """
      Unit Tests: 
        >>> client = RedditClient()
        >>> bundle = client.parseTitle('[GMG] Lego Star Wars: The Skywalker Saga Deluxe Edition - Steam Pre-order ($49.19/18% off)')
        >>> len(bundle.deals)
        1
        >>> bundle.merchant
        'GMG'
        >>> bundle.title
        'Lego Star Wars'
        >>> bundle.deals[0].title
        'The Skywalker Saga Deluxe Edition - Steam Pre-order'
        >>> bundle.deals[0].price
        '$49.19'
        >>> bundle.deals[0].discount
        '18%'
        >>> bundle.deals[0].price_gbp
        ''
        >>> bundle.deals[0].price_eur
        ''
        >>> bundle = client.parseTitle('[GMG] Lego Star Wars: The Skywalker Saga Deluxe Edition - Steam Pre-order ($49.19/-18%)')
        >>> bundle.deals[0].discount
        '18%'
        >>> bundle = client.parseTitle('[GMG] The Skywalker Saga Deluxe Edition - Steam Pre-order (17.5|€1.58|£1.18/-18% off)')
        >>> bundle.title
        ''
        >>> bundle.deals[0].title
        'The Skywalker Saga Deluxe Edition - Steam Pre-order'
        >>> bundle.deals[0].price
        ''
        >>> bundle.deals[0].price_eur
        '€1.58'
        >>> bundle.deals[0].price_gbp
        '£1.18'
        >>> bundle.deals[0].discount
        '18%'
        >>> bundle = client.parseTitle('[Steam] Toge Productions Anniversary Sale 2022: Coffee Talk (40%), Invalid Item, Rising Hell (-20%) and More')
        >>> bundle.merchant
        'Steam'
        >>> bundle.title
        'Toge Productions Anniversary Sale 2022'
        >>> len(bundle.deals)
        2
        >>> bundle.deals[0].title
        'Coffee Talk'
        >>> bundle.deals[0].discount
        '40%'
        >>> bundle.deals[1].title
        'Rising Hell'
        >>> bundle.deals[1].discount
        '20%'
      """
      bundle = Bundle()
      deals : List[Deal]=[]
      m = re.match(r"^\[(.+?)\] (.+)", title)
      if m is None:
        raise DoesNotFollowRulesException("Unexpected Title Format: " + title)
      else:
        bundle.merchant = m[1]
        deals_str = m[2]
        bundle_items = deals_str.split(':')
        if len(bundle_items) > 1:
          bundle.title = bundle_items[0]
          items_str = bundle_items[1]
        else:
          items_str = bundle_items[0]
          
        items = items_str.split(',')
        for item in items:
          deal : Deal = GameDeal()
          item = item.strip()
          m = re.match(r"^(.+?) \((.+?)\)", item)
          if m is None:
            continue
          deal.title = m[1]
          priceNpercent = m[2]
          m_price_dollar = re.search(r"\$\d+(\.\d+)?", priceNpercent)
          if m_price_dollar is not None:
            deal.price = m_price_dollar[0]
          m_price_pound = re.search(r"£\d+(\.\d+)?", priceNpercent)
          if m_price_pound is not None:
            deal.price_gbp = m_price_pound[0]
          m_price_euro = re.search(r"€\d+(\.\d+)?", priceNpercent)
          if m_price_euro is not None:
            deal.price_eur = m_price_euro[0]
          m_percent = re.search(r"\d+(\.\d+)?%", priceNpercent)
          if m_percent is not None:
            deal.discount = m_percent[0]
          deals.append(deal)
        bundle.deals = deals
        
        if len(bundle.deals) == 0:
          raise DoesNotFollowRulesException("Unexpected Title Format: " + title)
    
      return bundle

    def parseSubmissionByBody(self, subreddit_target: SubredditTarget, submission: praw.models.Submission) -> Bundle:
      """Looks for a table in praw.models.submission.selftext_html (body) and attempts to
      parse a list of deals.

      Args:
          submission (praw.models.Submission): A Submission object as defined by the PRAW API

      Returns:
          List[Deal]: A list of deals that are successfully parsed.
      """
      bundle = self.parseTableHtml(submission.selftext_html, subreddit_target)
      bundle.subreddit = subreddit_target
      bundle.url = submission.url
      bundle.date = datetime.datetime.fromtimestamp(submission.created).strftime("%m-%d-%Y")
      bundle.id = submission.id
      m = re.match(r"^\[(.+?)\] (.+)", submission.title)
      if m is None:
        raise DoesNotFollowRulesException("Unexpected Title Format: " + submission.title)
      else:
        bundle.merchant = m[1]
        bundle_items = m[2].split(':')
        if len(bundle_items) > 1:
          bundle.title = bundle_items[0]

      return bundle
      
    def parseTableHtml(self, html: str, subreddit_target: SubredditTarget) -> Bundle:
      """Scans a table and parses it for a Bundle containing a list of deals 

      Args:
          html (str): string of HTML parsable with bs4

      Returns:
          Bundle: bundle ontaining a list of successfully parsed Deals

      Unit Tests: 
        >>> client = RedditClient()
        >>> html = '<table class="MRH-njmSb5ZTkfb1o4dqv"><thead><tr class="s6JZe6869f81l9E_5G7Q9"><th class="_3TNkDptlyGOiWXvdX_acOB">Game</th><th class="_3TNkDptlyGOiWXvdX_acOB">Sale</th><th class="_3TNkDptlyGOiWXvdX_acOB">USD</th></tr></thead><tbody><tr class="s6JZe6869f81l9E_5G7Q9"><td class="_3DYfYn_cczg1wj_a3hhyV6">Dungeon of the Endless - Definitive Edition</td><td class="_3DYfYn_cczg1wj_a3hhyV6">80%</td><td class="_3DYfYn_cczg1wj_a3hhyV6">$3.99</td></tr><tr class="s6JZe6869f81l9E_5G7Q9"><td class="_3DYfYn_cczg1wj_a3hhyV6">Endless Legend - Monstrous Tales</td><td class="_3DYfYn_cczg1wj_a3hhyV6">33%</td><td class="_3DYfYn_cczg1wj_a3hhyV6">$2.00</td></tr></tbody></table>'
        >>> bundle = client.parseTableHtml(html=html, subreddit_target=SubredditTarget.GAMEDEALS)
        >>> len(bundle.deals) == 2
        True
      """
      bundle = Bundle()
      deals: List[Deal] = [] # result from parsing all tables
      soup = bs4.BeautifulSoup(html, features="html.parser")
      tables = soup.findAll('table')
      for table in tables:
        headers = [ header.text for header in table.findAll('th')]
        tvalues = [[ cell.text for cell in row.findAll('td')] for row in table.findAll('tr')][1:]
        for row in tvalues:
          deal: GameDeal = self.subreddit_deal_constructors[subreddit_target]()
          for index, value in enumerate(row):
            # Use the table headers to look up Deal attribute with synonyms
            deal.setAttribute(headers[index], value)
          if deal.isValid():
            deals.append(deal)
          else:
            raise DoesNotFollowRulesException("Unexpected Header Format: " + str(headers))

      bundle.deals = deals
      return bundle

    def extractDealsFromSubmission(self, 
                                   subreddit_target: SubredditTarget, 
                                   submission: praw.models.Submission) -> Bundle:
      if self.containsTable(submission):
        # attempt to parse the submission body 
        # look for tables while we are at it
        return self.parseSubmissionByBody(subreddit_target, submission)
      else:
        # attempt to parse the submission by title
        return self.parseSubmissionByTitle(subreddit_target, submission)

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
                limit:int = 1000,
                # Report success rate or not by default.
                report_success_rate: bool = False,
                # Display errors or not by default
                display_errors: bool = False) -> List[Bundle]:
      """
      Unit Tests:
        >>> client = RedditClient()
        >>> bundles = client.getDeals(limit=1, subreddit_target=SubredditTarget.GAMEDEALS)
        >>> len(bundles)
        1
      """
      bundles: List[Bundle] = []
      # Gets posts from subreddit_target filtered by subreddit_type limited to limit number of posts.
      successes = 0
      total = 0
      for submission in self.subreddit_function_table[subreddit_type](subreddit_target.value, limit):
        total = total + 1
        try:
          bundles.append(self.extractDealsFromSubmission(subreddit_target, submission))
          successes = successes + 1
        except DoesNotFollowRulesException as error:
          if display_errors == True:
            print(error.message)
      if report_success_rate == True:
        print(subreddit_type.value + ": " + str(successes/total*100) + "%")
      return bundles


    # Max sample_size is 1000. It will be capped at 1000 even if we set it higher.
    def getSuccessRate(self, subreddit_target: SubredditTarget, sample_size: int = 1000, display_errors: bool = False):
      """
        client = RedditClient()
        client.getSuccessRate(SubredditTarget.GAMEDEALS)
        SubredditFeedFilter.NEW: 97.7%
        SubredditFeedFilter.TOP: 100.0%
        SubredditFeedFilter.HOT: 86.2%
      """
      # Report success rate for NEW submissios
      self.getDeals(subreddit_target, SubredditFeedFilter.NEW, sample_size, True, display_errors)
      # Report success rate for TOP submissios
      self.getDeals(subreddit_target, SubredditFeedFilter.TOP, sample_size, True, display_errors)
      # Report success rate for HOT submissios
      self.getDeals(subreddit_target, SubredditFeedFilter.HOT, sample_size, True, display_errors)
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    client = RedditClient()
    client.getSuccessRate(SubredditTarget.GAMEDEALS, 500, True)
