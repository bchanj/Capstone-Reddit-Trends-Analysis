import praw


class reddit_client:
    """
    DOCSTRING
    """
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id="5J0BbjbzNZrNzSnZNOwCOQ",
            client_secret="JWno2YEOiAOhnY0tZDVtjGa6TWolTQ",
            password="ZhXEUe*k3qV2Ukf*vj3wuogD",
            user_agent="testscript",
            username="North-Alternative886",
        )

        self.reddit.read_only = True # change if editing

    def find_data(self, name):
        gd = self.reddit.subreddit(name)
        for submission in gd.hot(limit=5):
            print(submission.title)

