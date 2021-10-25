import installer
import os
installer.getDependencies() # Get dependencies before any imports

import argparse
from reddit.reddit_client import reddit_client
from reddit.MUAontheCheap_subreddit import MUAontheCheap
from sheets.gsheets_client import GSClient

if __name__ == "__main__":
    """
    Extract deals from reddit.
    """
    # Parse any flags and arguments here for extracting trends from reddit
    parser = argparse.ArgumentParser()
    sheet = GSClient()


