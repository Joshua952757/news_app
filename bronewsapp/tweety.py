import tweepy
from django.conf import settings

# Replace these values with your own credentials
API_KEY = settings.API_KEY
API_KEY_SECRET = settings.API_KEY_SECRET
ACCESS_TOKEN = settings.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = settings.ACCESS_TOKEN_SECRET
BEARER_TOKEN = settings.BEARER_TOKEN


def post_tweet(tweet_text):
    """Posts a tweet to Twitter."""
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_KEY_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )

    response = client.create_tweet(text=tweet_text)
    print("Tweet posted successfully!", response)
    return response