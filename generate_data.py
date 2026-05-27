"""
Script to generate a realistic synthetic dataset matching the
Reddit Posts on Depression in Indian Society dataset structure.
Run once to create: data/reddit_depression_india.csv
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

n = 2000

subreddits = ["depression", "India", "mentalhealth", "SuicideWatch",
              "Anxiety", "offmychest", "TrueOffMyChest", "depression_help"]
sentiments = ["Positive", "Negative", "Neutral"]
sentiment_weights = [0.18, 0.55, 0.27]
topics = ["Family Pressure", "Academic Stress", "Loneliness", "Relationship Issues",
          "Work Stress", "Social Stigma", "Financial Problems", "Identity Crisis",
          "Trauma", "Grief"]
flairs = ["Personal", "Support", "Rant", "Discussion", "Question", "Story", None]
age_groups = ["13-18", "19-24", "25-30", "31-40", "41+"]
genders = ["Male", "Female", "Non-binary", "Prefer not to say"]

titles_pool = [
    "Can't stop feeling hopeless about everything",
    "Indian family doesn't understand mental health",
    "Finally seeking help after years of suffering",
    "How do you deal with academic pressure?",
    "Society treats mental health like a weakness",
    "Struggling with loneliness in a metro city",
    "My parents think depression is just laziness",
    "Anyone else feel like a burden to their family?",
    "Success story: therapy actually helped me",
    "Is it normal to feel numb all the time?",
    "Why does no one talk about men's mental health in India?",
    "Lost my job and spiraling into depression",
    "Marriage pressure making everything worse",
    "IIT/IIM culture and its effect on mental health",
    "First time talking about this anywhere",
]

start_date = datetime(2021, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = (end_date - start_date).days

data = {
    "id": [f"t3_{random.randint(100000, 999999)}" for _ in range(n)],
    "title": [random.choice(titles_pool) + (" " + str(random.randint(1, 99)) if random.random() > 0.6 else "") for _ in range(n)],
    "subreddit": np.random.choice(subreddits, n, p=[0.25, 0.15, 0.18, 0.12, 0.10, 0.08, 0.07, 0.05]),
    "score": np.random.exponential(scale=80, size=n).astype(int).clip(0, 2000),
    "num_comments": np.random.exponential(scale=15, size=n).astype(int).clip(0, 300),
    "upvote_ratio": np.round(np.random.beta(8, 2, n), 2),
    "sentiment": np.random.choice(sentiments, n, p=sentiment_weights),
    "sentiment_score": np.round(np.random.uniform(-1, 1, n), 4),
    "topic": np.random.choice(topics, n),
    "flair": np.random.choice(flairs, n),
    "age_group": np.random.choice(age_groups, n, p=[0.10, 0.38, 0.28, 0.17, 0.07]),
    "gender": np.random.choice(genders, n, p=[0.52, 0.38, 0.05, 0.05]),
    "post_length": np.random.randint(20, 2000, n),
    "num_awards": np.random.choice([0,1,2,3,4,5], n, p=[0.70,0.15,0.08,0.04,0.02,0.01]),
    "is_selfpost": np.random.choice([True, False], n, p=[0.85, 0.15]),
    "created_utc": [start_date + timedelta(days=random.randint(0, date_range),
                                            hours=random.randint(0,23),
                                            minutes=random.randint(0,59)) for _ in range(n)],
}

df = pd.DataFrame(data)
df["created_date"] = pd.to_datetime(df["created_utc"]).dt.date
df["year"] = pd.to_datetime(df["created_utc"]).dt.year
df["month"] = pd.to_datetime(df["created_utc"]).dt.month
df["month_name"] = pd.to_datetime(df["created_utc"]).dt.strftime("%b")
df["day_of_week"] = pd.to_datetime(df["created_utc"]).dt.day_name()
df["hour"] = pd.to_datetime(df["created_utc"]).dt.hour

df.to_csv("/home/claude/dashboard_project/data/reddit_depression_india.csv", index=False)
print(f"Dataset saved: {len(df)} rows, {len(df.columns)} columns")
print(df.dtypes)
