# 🧠 Reddit Depression in Indian Society — EDA Dashboard

**Course:** Exploratory Data Analysis  
**Instructor:** Ali Hassan Sherazi  
**Submission Date:** 05-June-2026  

---

## 📁 Project Structure

```
dashboard_project/
├── data/
│   └── reddit_depression_india.csv   ← Dataset (DO NOT rename)
├── notebooks/
│   └── analysis.ipynb                ← EDA notebook
├── app.py                            ← Main Streamlit dashboard
├── charts.py                         ← All chart/visualization functions
├── filters.py                        ← Data loading & filtering functions
├── requirements.txt                  ← Python dependencies
└── README.md                         ← This file
```

---

## ⚙️ Installation & Running

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the dashboard
```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

---

## 📊 Charts Implemented

| # | Chart Type     | Variable(s) Used                        |
|---|----------------|-----------------------------------------|
| 1 | Pie Chart      | Sentiment distribution                  |
| 2 | Histogram      | Post length frequency                   |
| 3 | Line Chart     | Monthly post volume over time           |
| 4 | Bar Chart      | Posts per subreddit                     |
| 5 | Scatter Plot   | Score vs. Comments (by sentiment)       |
| 6 | Box Plot       | Score spread per sentiment category     |
| 7 | Heatmap        | Feature correlation matrix              |
| 8 | Area Chart     | Cumulative sentiment trends over time   |
| 9 | Count Plot     | Post count by discussion topic          |
|10 | Violin Plot    | Sentiment score distribution by category|
|🎁 | Bubble Chart  | Topic × Age Group (bonus)               |

---

## 🔍 Filters

- **Date Range** — Filter by post creation date
- **Subreddit** — Multi-select subreddits
- **Sentiment** — Positive / Negative / Neutral
- **Topic** — Discussion topic multi-select
- **Age Group** — Demographic filter
- **Gender** — Gender identity filter
- **Score Range** — Numerical slider
- **Text Search** — Keyword search in post titles
- **Reset Button** — Clears all filters

All filters are linked — every chart updates simultaneously when a filter is applied.

---

## 💡 Key Insights

1. **Negative sentiment dominates (~55%)** — reflecting the distressing nature of depression-related posts
2. **Family Pressure and Academic Stress** are the most frequently discussed topics, highlighting unique societal pressures in India
3. **The 19–24 age group** has the highest posting volume, indicating young adults are most vocal about mental health struggles
4. **Post volume increased year over year**, suggesting growing awareness and willingness to discuss mental health
5. **Positive sentiment posts tend to have higher scores and more comments**, possibly because they offer hope and attract engagement
6. **r/depression and r/mentalhealth** are the most active subreddits in this dataset

---

## 🛠 Tech Stack

| Tool       | Purpose                            |
|------------|------------------------------------|
| Python 3.x | Core language                      |
| Pandas     | Data loading, cleaning, filtering  |
| NumPy      | Numerical operations               |
| Matplotlib | Core chart creation                |
| Seaborn    | Statistical visualizations         |
| Streamlit  | Interactive frontend dashboard     |
