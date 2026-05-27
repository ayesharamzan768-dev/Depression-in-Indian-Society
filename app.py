"""
app.py - Main Dashboard Application
Reddit Posts on Depression in Indian Society
EDA Dashboard | Exploratory Data Analysis Course
Instructor: Ali Hassan Sherazi | Submission: 05-June-2026
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

# ── Page config ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Reddit Depression in India — EDA Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Dark background */
  .stApp { background-color: #0F1117; }
  section[data-testid="stSidebar"] { background-color: #161B27; }

  /* KPI cards */
  .kpi-card {
    background: #1C2130;
    border: 1px solid #2A3045;
    border-radius: 12px;
    padding: 18px 20px;
    text-align: center;
  }
  .kpi-label { font-size: 12px; color: #8892A4; text-transform: uppercase; letter-spacing: .08em; }
  .kpi-value { font-size: 30px; font-weight: 800; color: #E8ECF0; margin: 6px 0 2px; }
  .kpi-delta { font-size: 12px; }

  /* Section headers */
  .section-title {
    font-size: 15px; font-weight: 700; color: #4E8EF7;
    text-transform: uppercase; letter-spacing: .1em;
    border-left: 3px solid #4E8EF7; padding-left: 10px; margin: 18px 0 12px;
  }

  /* Tab active color override */
  div[data-baseweb="tab"] button[aria-selected="true"] { color: #4E8EF7 !important; }

  /* Data table */
  .stDataFrame { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Imports that need st.cache_data ───────────────────────────────────────
import filters as f
import charts as c

# ── Load data ─────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return f.load_data()

df_raw = get_data()

# ══════════════════════════════════════════════════════════════════════════
#  SIDEBAR FILTERS
# ══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("---")

    # Search / Text Filter
    search_text = st.text_input("🔎 Search Post Titles", placeholder="e.g. family, hopeless ...")

    st.markdown("**📅 Date Range**")
    min_date = df_raw["created_utc"].min().date()
    max_date = df_raw["created_utc"].max().date()
    date_start = st.date_input("From", value=min_date, min_value=min_date, max_value=max_date)
    date_end   = st.date_input("To",   value=max_date, min_value=min_date, max_value=max_date)

    # Category dropdowns
    all_subs = sorted(df_raw["subreddit"].unique())
    sel_subs = st.multiselect("📌 Subreddit", all_subs, default=all_subs)

    all_sent = sorted(df_raw["sentiment"].unique())
    sel_sent = st.multiselect("💬 Sentiment", all_sent, default=all_sent)

    all_topics = sorted(df_raw["topic"].unique())
    sel_topics = st.multiselect("🏷️ Topic", all_topics, default=all_topics)

    all_ages = ["13-18", "19-24", "25-30", "31-40", "41+"]
    sel_ages = st.multiselect("👤 Age Group", all_ages, default=all_ages)

    all_genders = sorted(df_raw["gender"].unique())
    sel_genders = st.multiselect("⚧ Gender", all_genders, default=all_genders)

    # Numerical range slider
    score_min = int(df_raw["score"].min())
    score_max = int(df_raw["score"].max())
    score_range = st.slider("📊 Post Score Range", score_min, score_max,
                            (score_min, score_max))

    st.markdown("---")
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()

# ── Apply filters ─────────────────────────────────────────────────────────
df = f.apply_filters(
    df_raw,
    date_range=(date_start, date_end),
    subreddits=sel_subs if sel_subs else None,
    sentiments=sel_sent if sel_sent else None,
    topics=sel_topics if sel_topics else None,
    age_groups=sel_ages if sel_ages else None,
    genders=sel_genders if sel_genders else None,
    score_range=score_range,
    search_text=search_text if search_text else None,
)

# ══════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style='padding: 10px 0 4px'>
  <span style='font-size:28px;font-weight:900;color:#E8ECF0;letter-spacing:-.02em'>
    🧠 Reddit Depression in Indian Society
  </span><br>
  <span style='font-size:13px;color:#8892A4'>
    Exploratory Data Analysis Dashboard &nbsp;·&nbsp; 
    Data: <em>reddit_depression_india.csv</em> &nbsp;·&nbsp; 
    Course: Exploratory Data Analysis &nbsp;·&nbsp; 
    Instructor: Ali Hassan Sherazi
  </span>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ── Filter status bar ─────────────────────────────────────────────────────
total_raw = len(df_raw)
total_filtered = len(df)
st.caption(f"Showing **{total_filtered:,}** of **{total_raw:,}** records after filters applied.")

if total_filtered == 0:
    st.warning("⚠️ No records match the current filter selection. Please adjust the filters.")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════
#  KPI SUMMARY CARDS
# ══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📌 Key Metrics</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">Total Posts</div>
      <div class="kpi-value">{total_filtered:,}</div>
    </div>""", unsafe_allow_html=True)

with k2:
    avg_score = df["score"].mean()
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">Avg Score</div>
      <div class="kpi-value">{avg_score:.1f}</div>
    </div>""", unsafe_allow_html=True)

with k3:
    avg_comments = df["num_comments"].mean()
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">Avg Comments</div>
      <div class="kpi-value">{avg_comments:.1f}</div>
    </div>""", unsafe_allow_html=True)

with k4:
    neg_pct = (df["sentiment"] == "Negative").mean() * 100
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">Negative Posts</div>
      <div class="kpi-value" style="color:#F76E6E">{neg_pct:.1f}%</div>
    </div>""", unsafe_allow_html=True)

with k5:
    top_topic = df["topic"].value_counts().idxmax()
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">Top Topic</div>
      <div class="kpi-value" style="font-size:16px;padding-top:7px">{top_topic}</div>
    </div>""", unsafe_allow_html=True)

with k6:
    max_score = df["score"].max()
    st.markdown(f"""<div class="kpi-card">
      <div class="kpi-label">Highest Score</div>
      <div class="kpi-value" style="color:#54C6A2">{max_score:,}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "📈 Trends & Distributions",
    "🔗 Relationships",
    "📋 Data Table"
])

# ── TAB 1: Overview ───────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-title">Sentiment & Topic Overview</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sentiment Distribution")
        st.pyplot(c.pie_chart_sentiment(df), use_container_width=True)

    with col2:
        st.subheader("Posts by Subreddit")
        st.pyplot(c.bar_chart_subreddits(df), use_container_width=True)

    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Discussion Topics (Count Plot)")
        st.pyplot(c.count_plot_topics(df), use_container_width=True)

    with col4:
        st.subheader("Bonus: Topic × Age Group (Bubble)")
        st.pyplot(c.bubble_chart_age_topic(df), use_container_width=True)

# ── TAB 2: Trends & Distributions ────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-title">Trends Over Time & Statistical Distributions</div>', unsafe_allow_html=True)

    st.subheader("Monthly Post Volume (Line Chart)")
    st.pyplot(c.line_chart_posts_over_time(df), use_container_width=True)

    st.subheader("Cumulative Sentiment Over Time (Area Chart)")
    st.pyplot(c.area_chart_sentiment_over_time(df), use_container_width=True)

    st.markdown("---")
    col5, col6 = st.columns(2)
    with col5:
        st.subheader("Post Length Distribution (Histogram)")
        st.pyplot(c.histogram_post_length(df), use_container_width=True)

    with col6:
        st.subheader("Score Distribution by Sentiment (Box Plot)")
        st.pyplot(c.box_plot_score_by_sentiment(df), use_container_width=True)

    st.subheader("Sentiment Score by Category (Violin Plot)")
    st.pyplot(c.violin_plot_sentiment_score(df), use_container_width=True)

# ── TAB 3: Relationships ──────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-title">Feature Relationships & Correlations</div>', unsafe_allow_html=True)

    col7, col8 = st.columns([1.1, 1])
    with col7:
        st.subheader("Score vs Comments (Scatter Plot)")
        st.pyplot(c.scatter_score_vs_comments(df), use_container_width=True)

    with col8:
        st.subheader("Feature Correlation Heatmap")
        st.pyplot(c.heatmap_correlation(df), use_container_width=True)

    st.markdown("---")
    # Summary stats table
    st.subheader("📐 Descriptive Statistics")
    num_cols = ["score", "num_comments", "upvote_ratio", "sentiment_score", "post_length", "num_awards"]
    st.dataframe(df[num_cols].describe().round(2), use_container_width=True)

# ── TAB 4: Data Table ─────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-title">Filtered Dataset Preview</div>', unsafe_allow_html=True)
    st.caption(f"{total_filtered:,} rows · {len(df.columns)} columns")

    display_cols = ["title", "subreddit", "sentiment", "topic", "score",
                    "num_comments", "upvote_ratio", "age_group", "gender",
                    "post_length", "created_date"]
    st.dataframe(df[display_cols].reset_index(drop=True), use_container_width=True, height=480)

    # Download button
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_reddit_depression.csv",
        mime="text/csv",
    )

# ── Footer ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#3A4255;font-size:11px'>"
    "EDA Dashboard Project · Exploratory Data Analysis · Instructor: Ali Hassan Sherazi · Due: 05-June-2026"
    "</div>",
    unsafe_allow_html=True
)
