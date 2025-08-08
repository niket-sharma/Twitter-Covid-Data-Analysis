# Twitter COVID Data Analysis

Utilities for collecting tweets related to COVID-19.

## Tweet scraper

The `covid_tweets.py` script retrieves tweets for a given search query and saves
them to a CSV file.

### Usage

1. Set your Twitter API credentials as environment variables:

```bash
export TWITTER_CONSUMER_KEY=... \
export TWITTER_CONSUMER_SECRET=... \
export TWITTER_ACCESS_TOKEN=... \
export TWITTER_ACCESS_TOKEN_SECRET=...
```

2. Run the scraper:

```bash
python covid_tweets.py "#SayNoToVaccines -filter:retweets" --limit 1000 --output scraped_tweets.csv
```

This command saves the tweets to `scraped_tweets.csv`.

### Dependencies

Install required packages with:

```bash
pip install -r requirements.txt
```
