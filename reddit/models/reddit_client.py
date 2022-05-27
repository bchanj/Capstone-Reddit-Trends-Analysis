#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "models"))

import praw
import re
import bs4
import datetime
import base64
import json
import dotenv
from enum import Enum
from typing import List, Dict
from deal import Deal, GameDeal
from subreddit_target import SubredditTarget
from subreddit_feed_filter import SubredditFeedFilter
from exceptions import DoesNotFollowRulesException

class RedditClient:
    """
    DOCSTRING
    """
    def __init__(self):
      super().__init__()
      self.DEFAULT_LIMIT=100
      self.reddit = self._prawCreateInstance()

      self.reddit.read_only = True # change if editing

      # Map of subreddit types to PRAW function for scraping
      self.subreddit_function_table: Dict[reddit.reddit_client.SubredditFeedFilter, function] = {
        SubredditFeedFilter.HOT: self.getHotSubmissions,
        SubredditFeedFilter.NEW: self.getNewSubmissions,
        SubredditFeedFilter.TOP: self.getTopSubmissions,
      }

    def _prawCreateInstance(self) -> praw.Reddit:
      dotenv.load_dotenv()
      encrypted_creds: str = os.environ["PRAW_CREDS"]
      decoded: bytes = base64.b64decode(encrypted_creds)
      json_dict = json.loads(decoded)
      return praw.Reddit(
        client_id=json_dict["client_id"],
        client_secret=json_dict["client_secret"],
        password=json_dict["password"],
        user_agent=json_dict["user_agent"],
        username=json_dict["username"],
      )

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
    # RAISES DoesNotFollowRulesException if unsuccessful
    def parseSubmissionByTitle(self, 
                              subreddit_target: SubredditTarget, 
                              submission: praw.models.Submission) -> List[Deal]:
      """Attempts to parse a list of deals from the submission title.

      Args:
          subreddit_target (SubredditTarget): The subreddit target 
          submission (praw.models.Submission): A Submission object as defined by the PRAW API

      Returns:
          list[Deal}: a list of successfully parsed Deals
      """
      url = submission.url
      date = datetime.datetime.fromtimestamp(submission.created).strftime("%m-%d-%Y")
      submission_id = submission.id
      title = submission.title
      deals = self.parseTitle(title, submission_id, url, date, subreddit_target)
      ### SOME PRINTS TO SHOW BUNDLE AND DEAL LEVEL WHEN WE PARSE TITLE
      #print("\nTitle: " + title)
      #print(deals)
      return deals

    def parseTitle(self,
                   title: str,
                   submission_id: str,
                   url: str,
                   date: str,
                   subreddit_target: SubredditTarget) -> List[Deal]:
      """
      Unit Tests: 
        >>> client = RedditClient()
        >>> deals = client.parseTitle('[GMG] Lego Star Wars: The Skywalker Saga Deluxe Edition - Steam Pre-order ($49.19/18% off)', 'abc', 'http://gamedeals', '2-21-2022', SubredditTarget.GAMEDEALS)
        >>> len(deals)
        1
        >>> deals[0].merchant
        'GMG'
        >>> deals[0].date
        '2-21-2022'
        >>> deals[0].url
        'http://gamedeals'
        >>> deals[0].bundle_id
        'abc'
        >>> deals[0].id
        'abc_1'
        >>> deals[0].bundle_title
        'Lego Star Wars'
        >>> deals[0].title
        'The Skywalker Saga Deluxe Edition - Steam Pre-order'
        >>> deals[0].price
        '$49.19'
        >>> deals[0].discount
        '18%'
        >>> deals[0].price_gbp
        ''
        >>> deals[0].price_eur
        ''
        >>> deals = client.parseTitle('[GMG] Lego Star Wars: The Skywalker Saga Deluxe Edition - Steam Pre-order ($49.19/-18%)', 'abc', 'http://gamedeals', '2-21-2022', SubredditTarget.GAMEDEALS)
        >>> deals[0].discount
        '18%'
        >>> deals = client.parseTitle('[GMG] The Skywalker Saga Deluxe Edition - Steam Pre-order (17.5|€1.58|£1.18/-18% off)', 'abc', 'http://gamedeals', '2-21-2022', SubredditTarget.GAMEDEALS)
        >>> len(deals)
        1
        >>> deals[0].bundle_title
        ''
        >>> deals[0].title
        'The Skywalker Saga Deluxe Edition - Steam Pre-order'
        >>> deals[0].price
        ''
        >>> deals[0].price_eur
        '€1.58'
        >>> deals[0].price_gbp
        '£1.18'
        >>> deals[0].discount
        '18%'
        >>> deals = client.parseTitle('[Steam] Toge Productions Anniversary Sale 2022: Coffee Talk (40%), Rising Hell (-20%) and More', 'abc', 'http://gamedeals', '2-21-2022', SubredditTarget.GAMEDEALS)
        >>> len(deals)
        2
        >>> deals[0].merchant
        'Steam'
        >>> deals[0].bundle_title
        'Toge Productions Anniversary Sale 2022'
        >>> deals[0].title
        'Coffee Talk'
        >>> deals[0].discount
        '40%'
        >>> deals[1].merchant
        'Steam'
        >>> deals[1].bundle_title
        'Toge Productions Anniversary Sale 2022'
        >>> deals[1].title
        'Rising Hell'
        >>> deals[1].discount
        '20%'
        >>> True
        False

        >>> deals = client.parseTitle('[Steam] Toge Productions Anniversary Sale 2022: Coffee Talk (%40)-- Free the people ($4,50):: Rising Hell (-20% 3,99$), Freedom Fighters (FREE) and More', 'abc', 'http://gamedeals', '2-21-2022', SubredditTarget.GAMEDEALS)
        >>> len(deals)
        4
        >>> deals[0].merchant
        'Steam'
        >>> deals[0].bundle_title
        'Toge Productions Anniversary Sale 2022'
        >>> deals[0].title
        'Coffee Talk'
        >>> deals[0].discount
        '%40'
        >>> deals[1].merchant
        'Steam'
        >>> deals[1].bundle_title
        'Toge Productions Anniversary Sale 2022'
        >>> deals[1].title
        'Free the people'
        >>> deals[1].price
        '$4,50'
        >>> deals[2].merchant
        'Steam'
        >>> deals[2].bundle_title
        'Toge Productions Anniversary Sale 2022'
        >>> deals[2].title
        'Rising Hell'
        >>> deals[2].discount
        '20%'
        >>> deals[2].price
        '3,99$'
        >>> deals[3].merchant
        'Steam'
        >>> deals[3].bundle_title
        'Toge Productions Anniversary Sale 2022'
        >>> deals[3].title
        'Freedom Fighters'
        >>> deals[3].price
        'FREE'
        """
      deals : List[Deal]=[]
      # Here we are parsing out the merchant, and the rest
      m = re.match(r"^\[(.+?)\] (.+)", title)
      if m is None:
        raise DoesNotFollowRulesException("Unexpected Title Format (missing merchant): " + title)
      else:
        merchant = m[1]
        deals_str = m[2]
        # Here we are parsing out the bundle title
        bundle_items = deals_str.split(':')
        if len(bundle_items) > 1:
          bundle_title = bundle_items[0]
          index = deals_str.index(':')
          items_str = deals_str[index + 1:]
        else:
          bundle_title = ''
          items_str = bundle_items[0]
        items = re.findall(r"(\W*(.+?) \((.*?\d.*?)\))|(\W*(.+?) \((.*?[Ff][Rr][Ee][Ee].*?)\))", items_str)
        item_index = 1
        for item in items:
          deal : Deal = GameDeal()
          deal.subreddit = subreddit_target.value
          deal.url = url
          deal.date = date
          deal.bundle_id = submission_id
          deal.id = submission_id + '_' + str(item_index)
          item_index = item_index + 1
          deal.title = item[1]
          if deal.title == '':
            deal.title = item[4]
          deal.bundle_title = bundle_title
          deal.merchant = merchant
          priceNpercent = item[2]
          if priceNpercent == '':
            priceNpercent = item[5]
          m_price_dollar = re.search(r"(\$\d+([,.]\d+)?)|(\d+([,.]\d+)?\$)|[Ff][Rr][Ee][Ee]", priceNpercent)
          if m_price_dollar is not None:
            deal.price = m_price_dollar[0]
          m_price_pound = re.search(r"(£\d+([,.]\d+)?)|(\d+([,.]\d+)?£)|[Ff][Rr][Ee][Ee]", priceNpercent)
          if m_price_pound is not None:
            deal.price_gbp = m_price_pound[0]
          m_price_euro = re.search(r"(€\d+([,.]\d+)?)|(\d+([,.]\d+)?€)|[Ff][Rr][Ee][Ee]", priceNpercent)
          if m_price_euro is not None:
            deal.price_eur = m_price_euro[0]
          m_percent = re.search(r"(\d+([,.]\d+)?%)|(%\d+([,.]\d+)?)", priceNpercent)
          if m_percent is not None:
            deal.discount = m_percent[0]
          if deal.isValid():
            deals.append(deal)
        
      if len(deals) == 0:
        raise DoesNotFollowRulesException("Unexpected Title Format (no valid deals in title): " + title)
    
      return deals

    def parseSubmissionByBody(self,
                              subreddit_target: SubredditTarget,
                              submission: praw.models.Submission) -> List[Deal]:
      """Looks for a table in praw.models.submission.selftext_html (body) and attempts to
      parse a list of deals.

      Args:
          subreddit_target (SubredditTarget): The subreddit target 
          submission (praw.models.Submission): A Submission object as defined by the PRAW API

      Returns:
          list[Deal}: a list of successfully parsed Deals
      """
      html = submission.selftext_html
      url = submission.url
      date = datetime.datetime.fromtimestamp(submission.created).strftime("%m-%d-%Y")
      submission_id = submission.id
      title = submission.title
      deals = self.parseTableHtml(subreddit_target, html, url, date, submission_id, title)
      ### SOME PRINTS TO SHOW BUNDLE AND DEAL LEVEL WHEN WE PARSE TABLE
      #print("\nTable: " + html)
      #print("Title: " + title)
      #print(deals)
      return deals
      
    def parseTableHtml(self,
                       subreddit_target: SubredditTarget,
                       html: str,
                       url: str,
                       date: str,
                       submission_id: str,
                       title: str) -> List[Deal]:
      """Looks for a table in praw.models.submission.selftext_html (body) and attempts to
      parse a list of deals.

      Returns:
          list[Deal}: a list of successfully parsed Deals

      Unit Tests: 
        >>> client = RedditClient()
        >>> html = '<table class="MRH-njmSb5ZTkfb1o4dqv"><thead><tr class="s6JZe6869f81l9E_5G7Q9"><th class="_3TNkDptlyGOiWXvdX_acOB">Game</th><th class="_3TNkDptlyGOiWXvdX_acOB">Sale</th><th class="_3TNkDptlyGOiWXvdX_acOB">USD</th></tr></thead><tbody><tr class="s6JZe6869f81l9E_5G7Q9"><td class="_3DYfYn_cczg1wj_a3hhyV6">Dungeon of the Endless - Definitive Edition</td><td class="_3DYfYn_cczg1wj_a3hhyV6">80%</td><td class="_3DYfYn_cczg1wj_a3hhyV6">$3.99</td></tr><tr class="s6JZe6869f81l9E_5G7Q9"><td class="_3DYfYn_cczg1wj_a3hhyV6">Endless Legend - Monstrous Tales</td><td class="_3DYfYn_cczg1wj_a3hhyV6">33%</td><td class="_3DYfYn_cczg1wj_a3hhyV6">$2.00</td></tr></tbody></table>'
        >>> deals = client.parseTableHtml(SubredditTarget.GAMEDEALS, html, 'http://gamedeals', '2-21-2022', 'abc', '[Nintendo] Thxgiving Deals: etc etc')
        >>> len(deals) == 2
        True
        >>> deals[0].merchant
        'Nintendo'
        >>> deals[0].date
        '2-21-2022'
        >>> deals[0].url
        'http://gamedeals'
        >>> deals[0].bundle_id
        'abc'
        >>> deals[0].id
        'abc_1'
        >>> deals[0].bundle_title
        'Thxgiving Deals'
        >>> deals[0].title
        'Dungeon of the Endless - Definitive Edition'
        >>> deals[0].price
        '$3.99'
        >>> deals[1].merchant
        'Nintendo'
        >>> deals[1].date
        '2-21-2022'
        >>> deals[1].url
        'http://gamedeals'
        >>> deals[1].bundle_id
        'abc'
        >>> deals[1].id
        'abc_2'
        >>> deals[1].bundle_title
        'Thxgiving Deals'
        >>> deals[1].title
        'Endless Legend - Monstrous Tales'
        >>> deals[1].price
        '$2.00'
      """
      deals: List[Deal] = [] # result from parsing all tables
      subreddit = subreddit_target.value
      # We parse some of the deal attributes from the title
      title_m = re.match(r"^\[(.+?)\] (.+)", title)
      if title_m is None:
        raise DoesNotFollowRulesException("Unexpected Title Format (missing merchant): " + title)
      else:
        merchant = title_m[1]
        bundle_items = title_m[2].split(':')
        bundle_title = ''
        if len(bundle_items) > 1:
          bundle_title = bundle_items[0]
          
      # Most deal attributes come from the table
      soup = bs4.BeautifulSoup(html, features="html.parser")
      tables = soup.findAll('table')
      deal_index = 1
      headers = []

      for table in tables:
        headers = [ header.text for header in table.findAll('th')]
        for row in table.findAll('tr')[1:]:
          deal: GameDeal = GameDeal()
          deal.subreddit = subreddit
          deal.url = url
          for link in row.findAll('a'):
            if link.has_attr('href'):
                deal.url = link['href']
          deal.date = date
          deal.merchant = merchant
          deal.bundle_title = bundle_title
          deal.bundle_id = submission_id
          deal.id = submission_id + '_' + str(deal_index)
          deal_index = deal_index + 1
          cell_content = [ cell.text for cell in row.findAll('td') ]
          for index, value in enumerate(cell_content):
            # Use the table headers to look up Deal attribute with synonyms
            deal.setAttribute(headers[index], value)
          if deal.isValid():
            deals.append(deal)

        # tvalues = [[ cell.text for cell in row.findAll('td')] for row in table.findAll('tr')][1:]
        # for row in tvalues:
        #   deal: GameDeal = GameDeal()
        #   deal.subreddit = subreddit
        #   deal.url = url
        #   deal.date = date
        #   deal.merchant = merchant
        #   deal.bundle_title = bundle_title
        #   deal.bundle_id = submission_id
        #   deal.id = submission_id + '_' + str(deal_index)
        #   deal_index = deal_index + 1
        #   for index, value in enumerate(row):
        #     # Use the table headers to look up Deal attribute with synonyms
        #     deal.setAttribute(headers[index], value)
        #   if deal.isValid():
        #     deals.append(deal)

      if len(deals) == 0:
        raise DoesNotFollowRulesException("Unexpected Header Format: " + str(headers) + ' for the post titled: ' + title)

      return deals

    def extractDealsFromSubmission(self, 
                                   subreddit_target: SubredditTarget, 
                                   submission: praw.models.Submission) -> List[Deal]:
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
                limit:int = 10,
                # Report success rate or not by default.
                report_success_rate: bool = False,
                # Display errors or not by default
                display_errors: bool = False) -> List[Deal]:
      """
      Unit Tests:
        >>> client = RedditClient()
        >>> deals = client.getDeals(limit=1, subreddit_target=SubredditTarget.GAMEDEALS)
        >>> len(deals) >= 1
        True
      """
      deals: List[Deal] = []
      # Gets posts from subreddit_target filtered by subreddit_type limited to limit number of posts.
      successes = 0
      total = 0
      for submission in self.subreddit_function_table[subreddit_type](subreddit_target.value, limit):
        total = total + 1
        try:
          deals.extend(self.extractDealsFromSubmission(subreddit_target, submission))
          successes = successes + 1
        except DoesNotFollowRulesException as error:
          if display_errors == True:
            print(error.message)
      if report_success_rate == True:
        print(subreddit_type.value + ": " + str(successes/total*100) + "%\n")
      return deals

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