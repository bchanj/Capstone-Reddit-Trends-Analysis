import installer
import argparse
from reddit.reddit_client import reddit_client

if __name__ == "__main__":
    """
    Extract deals from reddit.
    """
    # Check for dependencies before we run any commands
    installer.getDependencies()

    parser = argparse.ArgumentParser()
    # Parse any flags and arguments here for extracting trends from reddit
    client = reddit_client()
    client.get_sub_reddit_submissions("GameDeals")
