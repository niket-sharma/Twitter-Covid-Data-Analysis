"""Utility for scraping tweets related to COVID-19 hashtags.

This module exposes a command line interface for collecting tweets that match a
given search query. API credentials are read from the following environment
variables:

- TWITTER_CONSUMER_KEY
- TWITTER_CONSUMER_SECRET
- TWITTER_ACCESS_TOKEN
- TWITTER_ACCESS_TOKEN_SECRET
"""

from __future__ import annotations

import argparse
import os
from typing import List

import pandas as pd
import tweepy


def create_api() -> tweepy.API:
    """Create a Tweepy API instance using credentials stored in environment variables.

    Raises:
        RuntimeError: If any of the required credentials are missing.
    """
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    if not all([consumer_key, consumer_secret, access_token, access_secret]):
        raise RuntimeError(
            "Twitter API credentials are not fully set in environment variables."
        )

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return tweepy.API(auth, wait_on_rate_limit=True)


def tweet_to_row(tweet: tweepy.Status) -> List:
    """Convert a Tweepy Status object to a list representing one CSV row."""
    hashtags = [h["text"] for h in tweet.entities.get("hashtags", [])]
    try:
        text = tweet.retweeted_status.full_text
    except AttributeError:
        text = tweet.full_text

    return [
        tweet.user.screen_name,
        tweet.user.description,
        tweet.user.location,
        tweet.user.friends_count,
        tweet.user.followers_count,
        tweet.user.statuses_count,
        tweet.retweet_count,
        text,
        hashtags,
    ]


def scrape_tweets(api: tweepy.API, query: str, limit: int) -> pd.DataFrame:
    """Collect tweets matching *query*.

    Args:
        api: Tweepy API instance.
        query: Search query passed to the Twitter API.
        limit: Maximum number of tweets to retrieve.

    Returns:
        DataFrame containing information for each tweet.
    """
    columns = [
        "username",
        "description",
        "location",
        "following",
        "followers",
        "totaltweets",
        "retweetcount",
        "text",
        "hashtags",
    ]
    cursor = tweepy.Cursor(
        api.search, q=query, lang="en", tweet_mode="extended"
    ).items(limit)

    rows = [tweet_to_row(tweet) for tweet in cursor]
    return pd.DataFrame(rows, columns=columns)


def save_to_csv(df: pd.DataFrame, filename: str) -> None:
    """Save the DataFrame *df* to CSV format."""
    df.to_csv(filename, index=False)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape tweets for a given search query."
    )
    parser.add_argument(
        "query", help="Twitter search query, e.g. '#SayNoToVaccines -filter:retweets'"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of tweets to collect (default: 100).",
    )
    parser.add_argument(
        "--output",
        default="scraped_tweets.csv",
        help="Filename for the resulting CSV (default: scraped_tweets.csv).",
    )
    args = parser.parse_args()

    api = create_api()
    df = scrape_tweets(api, args.query, args.limit)
    save_to_csv(df, args.output)
    print("Scraping has completed!")


if __name__ == "__main__":
    main()
