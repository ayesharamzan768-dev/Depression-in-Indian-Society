"""
filters.py - Data loading, cleaning, and filtering functions
EDA Dashboard Project - Reddit Depression in Indian Society
"""

import pandas as pd
import numpy as np

DATA_PATH = "data/reddit_depression_india.csv"


def load_data():
    """Load and clean the dataset."""
    df = pd.read_csv(DATA_PATH)
    df["created_utc"] = pd.to_datetime(df["created_utc"])
    df["created_date"] = pd.to_datetime(df["created_date"])
    df["flair"] = df["flair"].fillna("Unflaired")
    df["post_length"] = df["post_length"].clip(lower=0)
    df["score"] = df["score"].clip(lower=0)
    return df


def apply_filters(df, date_range=None, subreddits=None, sentiments=None,
                  topics=None, age_groups=None, genders=None,
                  score_range=None, search_text=None):
    """Apply all sidebar filters and return filtered dataframe."""
    filtered = df.copy()

    if date_range and len(date_range) == 2:
        start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        filtered = filtered[(filtered["created_utc"] >= start) & (filtered["created_utc"] <= end)]

    if subreddits:
        filtered = filtered[filtered["subreddit"].isin(subreddits)]

    if sentiments:
        filtered = filtered[filtered["sentiment"].isin(sentiments)]

    if topics:
        filtered = filtered[filtered["topic"].isin(topics)]

    if age_groups:
        filtered = filtered[filtered["age_group"].isin(age_groups)]

    if genders:
        filtered = filtered[filtered["gender"].isin(genders)]

    if score_range:
        filtered = filtered[(filtered["score"] >= score_range[0]) & (filtered["score"] <= score_range[1])]

    if search_text and search_text.strip():
        mask = filtered["title"].str.contains(search_text.strip(), case=False, na=False)
        filtered = filtered[mask]

    return filtered
