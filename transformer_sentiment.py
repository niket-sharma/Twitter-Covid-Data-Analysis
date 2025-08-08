"""Sentiment analysis for tweets using a transformer model.

This script reads a CSV file of tweets that contains a ``text`` column and
produces a new CSV with sentiment labels and scores. It relies on a
state-of-the-art RoBERTa model fine-tuned for Twitter sentiment analysis.
"""

from __future__ import annotations

import argparse
from typing import List

import pandas as pd
from transformers import pipeline


MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"


def load_tweets(filename: str) -> List[str]:
    """Return the tweets stored in *filename*.

    Args:
        filename: Path to a CSV file containing a ``text`` column.

    Returns:
        List of tweet texts.

    Raises:
        RuntimeError: If the ``text`` column is missing.
    """
    df = pd.read_csv(filename)
    if "text" not in df.columns:
        raise RuntimeError("Input CSV must contain a 'text' column")
    return df["text"].tolist()


def analyze_sentiment(texts: List[str]) -> pd.DataFrame:
    """Analyze sentiment for each item in *texts* using a transformer model."""
    classifier = pipeline("sentiment-analysis", model=MODEL_NAME, device=-1)
    results = classifier(texts, truncation=True)
    return pd.DataFrame(results)


def save_results(texts: List[str], results: pd.DataFrame, output_file: str) -> None:
    """Save *results* alongside *texts* to *output_file* in CSV format."""
    output_df = pd.DataFrame({"text": texts, "label": results["label"], "score": results["score"]})
    output_df.to_csv(output_file, index=False)


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Analyze tweet sentiment using a pre-trained transformer model."
    )
    parser.add_argument("input", help="CSV file containing tweets in a 'text' column")
    parser.add_argument(
        "--output",
        default="sentiment_results.csv",
        help="Filename for the CSV with sentiment labels (default: sentiment_results.csv)",
    )
    args = parser.parse_args(argv)

    texts = load_tweets(args.input)
    results = analyze_sentiment(texts)
    save_results(texts, results, args.output)
    print(f"Sentiment analysis complete: {args.output}")


if __name__ == "__main__":
    main()
