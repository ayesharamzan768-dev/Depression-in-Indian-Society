"""
charts.py - Chart and visualization functions
EDA Dashboard Project - Reddit Depression in Indian Society
Uses Matplotlib + Seaborn as required.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
import numpy as np

# ── Consistent professional color palette ──────────────────────────────────
PALETTE      = ["#4E8EF7", "#F76E6E", "#54C6A2", "#F7C04A", "#9B7FE8",
                "#F4845F", "#52B8D4", "#A3D977", "#E87EC0", "#7EC8C8"]
BG_COLOR     = "#0F1117"
CARD_COLOR   = "#1C2130"
TEXT_COLOR   = "#E8ECF0"
ACCENT       = "#4E8EF7"
NEG_COLOR    = "#F76E6E"
POS_COLOR    = "#54C6A2"
NEUTRAL_COLOR= "#F7C04A"
GRID_COLOR   = "#2A3045"

def _base_style():
    """Apply consistent dark-theme style."""
    plt.rcParams.update({
        "figure.facecolor":  BG_COLOR,
        "axes.facecolor":    CARD_COLOR,
        "axes.edgecolor":    GRID_COLOR,
        "axes.labelcolor":   TEXT_COLOR,
        "axes.titlecolor":   TEXT_COLOR,
        "axes.titlesize":    13,
        "axes.labelsize":    11,
        "xtick.color":       TEXT_COLOR,
        "ytick.color":       TEXT_COLOR,
        "xtick.labelsize":   9,
        "ytick.labelsize":   9,
        "legend.facecolor":  CARD_COLOR,
        "legend.edgecolor":  GRID_COLOR,
        "legend.fontsize":   9,
        "legend.labelcolor": TEXT_COLOR,
        "grid.color":        GRID_COLOR,
        "grid.linestyle":    "--",
        "grid.alpha":        0.5,
        "text.color":        TEXT_COLOR,
        "font.family":       "DejaVu Sans",
    })

# ── 1. PIE CHART ───────────────────────────────────────────────────────────
def pie_chart_sentiment(df):
    _base_style()
    counts = df["sentiment"].value_counts()
    colors = {"Positive": POS_COLOR, "Negative": NEG_COLOR, "Neutral": NEUTRAL_COLOR}
    c = [colors.get(s, ACCENT) for s in counts.index]
    fig, ax = plt.subplots(figsize=(6, 5), facecolor=BG_COLOR)
    wedges, texts, autotexts = ax.pie(
        counts, labels=counts.index, autopct="%1.1f%%",
        colors=c, startangle=140, pctdistance=0.75,
        wedgeprops=dict(edgecolor=BG_COLOR, linewidth=2)
    )
    for t in texts:    t.set_color(TEXT_COLOR); t.set_fontsize(10)
    for a in autotexts: a.set_color(BG_COLOR); a.set_fontweight("bold"); a.set_fontsize(9)
    ax.set_facecolor(BG_COLOR)
    ax.set_title("Sentiment Distribution of Posts", pad=12)
    fig.tight_layout()
    return fig

# ── 2. HISTOGRAM ───────────────────────────────────────────────────────────
def histogram_post_length(df):
    _base_style()
    fig, ax = plt.subplots(figsize=(7, 4), facecolor=BG_COLOR)
    ax.hist(df["post_length"].clip(0, 1500), bins=40, color=ACCENT, edgecolor=BG_COLOR, alpha=0.85)
    ax.set_xlabel("Post Length (characters)")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution of Post Lengths")
    ax.axvline(df["post_length"].median(), color=NEG_COLOR, linestyle="--", linewidth=1.5, label=f'Median: {df["post_length"].median():.0f}')
    ax.legend()
    ax.yaxis.grid(True); ax.set_axisbelow(True)
    fig.tight_layout()
    return fig

# ── 3. LINE CHART ──────────────────────────────────────────────────────────
def line_chart_posts_over_time(df):
    _base_style()
    monthly = df.groupby(df["created_utc"].dt.to_period("M")).size().reset_index()
    monthly.columns = ["period", "count"]
    monthly["period_str"] = monthly["period"].astype(str)
    fig, ax = plt.subplots(figsize=(9, 4), facecolor=BG_COLOR)
    ax.plot(monthly["period_str"], monthly["count"], color=ACCENT, linewidth=2.2, marker="o", markersize=4)
    ax.fill_between(range(len(monthly)), monthly["count"], alpha=0.12, color=ACCENT)
    step = max(1, len(monthly) // 8)
    ax.set_xticks(range(0, len(monthly), step))
    ax.set_xticklabels(monthly["period_str"].iloc[::step], rotation=30, ha="right")
    ax.set_xlabel("Month"); ax.set_ylabel("Number of Posts")
    ax.set_title("Monthly Post Volume Over Time")
    ax.yaxis.grid(True); ax.set_axisbelow(True)
    fig.tight_layout()
    return fig

# ── 4. BAR CHART ───────────────────────────────────────────────────────────
def bar_chart_subreddits(df):
    _base_style()
    counts = df["subreddit"].value_counts().head(8)
    fig, ax = plt.subplots(figsize=(8, 4), facecolor=BG_COLOR)
    bars = ax.barh(counts.index[::-1], counts.values[::-1], color=PALETTE[:len(counts)], edgecolor=BG_COLOR)
    for bar, val in zip(bars, counts.values[::-1]):
        ax.text(val + max(counts)*0.01, bar.get_y() + bar.get_height()/2,
                str(val), va="center", fontsize=9, color=TEXT_COLOR)
    ax.set_xlabel("Number of Posts"); ax.set_title("Posts by Subreddit")
    ax.xaxis.grid(True); ax.set_axisbelow(True)
    fig.tight_layout()
    return fig

# ── 5. SCATTER PLOT ────────────────────────────────────────────────────────
def scatter_score_vs_comments(df):
    _base_style()
    sample = df.sample(min(500, len(df)), random_state=1)
    colors = {"Positive": POS_COLOR, "Negative": NEG_COLOR, "Neutral": NEUTRAL_COLOR}
    c = [colors.get(s, ACCENT) for s in sample["sentiment"]]
    fig, ax = plt.subplots(figsize=(7, 5), facecolor=BG_COLOR)
    ax.scatter(sample["score"], sample["num_comments"], c=c, alpha=0.55, s=25, edgecolors="none")
    handles = [mpatches.Patch(color=v, label=k) for k, v in colors.items()]
    ax.legend(handles=handles, title="Sentiment")
    ax.set_xlabel("Post Score"); ax.set_ylabel("Number of Comments")
    ax.set_title("Score vs. Comments (colored by Sentiment)")
    ax.yaxis.grid(True); ax.xaxis.grid(True); ax.set_axisbelow(True)
    fig.tight_layout()
    return fig

# ── 6. BOX PLOT ────────────────────────────────────────────────────────────
def box_plot_score_by_sentiment(df):
    _base_style()
    fig, ax = plt.subplots(figsize=(7, 5), facecolor=BG_COLOR)
    order = ["Positive", "Neutral", "Negative"]
    palette = {"Positive": POS_COLOR, "Neutral": NEUTRAL_COLOR, "Negative": NEG_COLOR}
    data_groups = [df[df["sentiment"] == s]["score"].clip(0, 500) for s in order]
    bp = ax.boxplot(data_groups, labels=order, patch_artist=True,
                    medianprops=dict(color=TEXT_COLOR, linewidth=2),
                    whiskerprops=dict(color=GRID_COLOR),
                    capprops=dict(color=GRID_COLOR),
                    flierprops=dict(marker=".", color=GRID_COLOR, markersize=3, alpha=0.4))
    for patch, s in zip(bp["boxes"], order):
        patch.set_facecolor(palette[s]); patch.set_alpha(0.75)
    ax.set_ylabel("Post Score"); ax.set_title("Score Distribution by Sentiment")
    ax.yaxis.grid(True); ax.set_axisbelow(True)
    fig.tight_layout()
    return fig

# ── 7. HEATMAP ────────────────────────────────────────────────────────────
def heatmap_correlation(df):
    _base_style()
    num_cols = ["score", "num_comments", "upvote_ratio", "sentiment_score",
                "post_length", "num_awards"]
    corr = df[num_cols].corr()
    fig, ax = plt.subplots(figsize=(7, 5.5), facecolor=BG_COLOR)
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                ax=ax, linewidths=0.5, linecolor=BG_COLOR,
                annot_kws={"size": 9},
                cbar_kws={"shrink": 0.8})
    ax.set_title("Feature Correlation Heatmap")
    ax.set_facecolor(CARD_COLOR)
    plt.xticks(rotation=30, ha="right"); plt.yticks(rotation=0)
    fig.tight_layout()
    return fig

# ── 8. AREA CHART ─────────────────────────────────────────────────────────
def area_chart_sentiment_over_time(df):
    _base_style()
    monthly = (df.groupby([df["created_utc"].dt.to_period("M"), "sentiment"])
               .size().unstack(fill_value=0).reset_index())
    monthly["period_str"] = monthly["created_utc"].astype(str)
    fig, ax = plt.subplots(figsize=(9, 4.5), facecolor=BG_COLOR)
    x = range(len(monthly))
    colors = {"Positive": POS_COLOR, "Negative": NEG_COLOR, "Neutral": NEUTRAL_COLOR}
    bottom = np.zeros(len(monthly))
    for sent in ["Negative", "Neutral", "Positive"]:
        if sent in monthly.columns:
            ax.fill_between(x, bottom, bottom + monthly[sent], label=sent,
                            color=colors.get(sent, ACCENT), alpha=0.8)
            bottom += monthly[sent].values
    step = max(1, len(monthly) // 8)
    ax.set_xticks(range(0, len(monthly), step))
    ax.set_xticklabels(monthly["period_str"].iloc[::step], rotation=30, ha="right")
    ax.set_xlabel("Month"); ax.set_ylabel("Post Count")
    ax.set_title("Cumulative Sentiment Trend Over Time")
    ax.legend(loc="upper left"); ax.yaxis.grid(True); ax.set_axisbelow(True)
    fig.tight_layout()
    return fig

# ── 9. COUNT PLOT ─────────────────────────────────────────────────────────
def count_plot_topics(df):
    _base_style()
    order = df["topic"].value_counts().index.tolist()
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=BG_COLOR)
    sns.countplot(data=df, y="topic", order=order, hue="topic", palette=PALETTE,
                  legend=False, ax=ax, edgecolor=BG_COLOR)
    ax.set_xlabel("Count"); ax.set_ylabel("Topic")
    ax.set_title("Post Count by Discussion Topic")
    ax.xaxis.grid(True); ax.set_axisbelow(True)
    fig.tight_layout()
    return fig

# ── 10. VIOLIN PLOT ───────────────────────────────────────────────────────
def violin_plot_sentiment_score(df):
    _base_style()
    fig, ax = plt.subplots(figsize=(7, 5), facecolor=BG_COLOR)
    order = ["Positive", "Neutral", "Negative"]
    palette = {"Positive": POS_COLOR, "Neutral": NEUTRAL_COLOR, "Negative": NEG_COLOR}
    sns.violinplot(data=df, x="sentiment", y="sentiment_score", order=order, hue="sentiment", legend=False,
                   palette=palette, ax=ax, inner="quartile",
                   linewidth=1.2)
    ax.set_title("Sentiment Score Distribution by Category")
    ax.set_xlabel("Sentiment"); ax.set_ylabel("Sentiment Score")
    ax.yaxis.grid(True); ax.set_axisbelow(True)
    ax.axhline(0, color=GRID_COLOR, linewidth=1, linestyle="--")
    fig.tight_layout()
    return fig

# ── BONUS: BUBBLE CHART ───────────────────────────────────────────────────
def bubble_chart_age_topic(df):
    _base_style()
    pivot = df.groupby(["age_group", "topic"]).size().reset_index(name="count")
    age_order = ["13-18", "19-24", "25-30", "31-40", "41+"]
    pivot["age_idx"] = pivot["age_group"].map({a: i for i, a in enumerate(age_order)})
    pivot["topic_idx"] = pivot["topic"].astype("category").cat.codes
    topic_labels = pivot[["topic_idx", "topic"]].drop_duplicates().sort_values("topic_idx")
    fig, ax = plt.subplots(figsize=(9, 5.5), facecolor=BG_COLOR)
    sc = ax.scatter(pivot["age_idx"], pivot["topic_idx"],
                    s=pivot["count"] * 12, c=pivot["count"],
                    cmap="Blues", alpha=0.8, edgecolors=GRID_COLOR, linewidth=0.5)
    ax.set_xticks(range(len(age_order))); ax.set_xticklabels(age_order)
    ax.set_yticks(topic_labels["topic_idx"]); ax.set_yticklabels(topic_labels["topic"])
    ax.set_xlabel("Age Group"); ax.set_ylabel("Topic")
    ax.set_title("Bubble Chart: Topic vs Age Group (size = post count)")
    plt.colorbar(sc, ax=ax, label="Post Count", shrink=0.8)
    ax.yaxis.grid(True); ax.xaxis.grid(True); ax.set_axisbelow(True)
    fig.tight_layout()
    return fig
