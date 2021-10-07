import installer
installer.getDependencies() # Get dependencies before any imports

import argparse
from reddit.reddit_client import reddit_client

if __name__ == "__main__":
    """
    Extract deals from reddit.
    """
    # Parse any flags and arguments here for extracting trends from reddit
    parser = argparse.ArgumentParser()