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
        self.reddit.read_only = True

    def get_sub_reddit(self, sub_reddit_name: str):
        return self.reddit.subreddit(sub_reddit_name)

    def get_sub_reddit_submissions(self, sub_reddit_name: str):
        subreddit = self.get_sub_reddit(sub_reddit_name)
        # assume you have a Subreddit instance bound to variable `subreddit`
        for submission in subreddit.hot(limit=10):
            print(submission.title)
            # Output: the submission's title
            print(submission.score)
            # Output: the submission's score
            print(submission.id)
            # Output: the submission's ID
            print(submission.url)
            # Output: the URL the submission points to or the submission's URL if it's a self post
    