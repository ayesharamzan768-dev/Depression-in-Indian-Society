import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Apply a professional visual style globally
sns.set_theme(style="whitegrid")
plt.rcParams.update({'figure.max_open_warning': 0, 'font.size': 10})

def generate_all_charts(df):
    charts = {}
    if df.empty:
        return charts

    # 1. Pie Chart (Distribution of cases by Province)
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    prov_data = df.groupby('Province').sum()
    ax1.pie(prov_data, labels=prov_data.index, autopct='%1.1f%%', colors=sns.color_palette('Pastel1'), startangle=90)
    ax1.set_title("Distribution of Confirmed Cases by Province")
    charts['pie'] = fig1

    # 2. Histogram (Frequency distribution of Rainfall Anomaly)
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.histplot(data=df, x='Rainfall_Anomaly_mm', kde=True, color='skyblue', bins=10, ax=ax2)
    ax2.set_title("Frequency Distribution of Rainfall Anomaly (mm)")
    ax2.set_xlabel("Rainfall Anomaly (mm)")
    charts['hist'] = fig2

    # 3. Line Chart (Trends over time)
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    yearly = df.groupby('Year')].sum().reset_index()
    sns.lineplot(data=yearly, x='Year', y='Estimated_Cases_WHO', marker='o', label='WHO Estimated', color='red', ax=ax3)
    sns.lineplot(data=yearly, x='Year', y='Reported_Confirmed_Cases', marker='s', label='Reported Confirmed', color='navy', ax=ax3)
    ax3.set_title("Malaria Cases Trajectory Over Time")
    ax3.set_ylabel("Number of Cases")
    charts['line'] = fig3

    # 4. Bar Chart (Compare deaths across provinces)
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    sns.barplot(data=df, x='Province', y='Reported_Deaths', estimator=np.sum, palette='muted', hue='Province', legend=False, ax=ax4)
    ax4.set_title("Total Reported Deaths by Region")
    ax4.set_ylabel("Total Deaths")
    charts['bar'] = fig4

    # 5. Scatter Plot (Rainfall Anomaly vs. Confirmed Cases)
    fig5, ax5 = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=df, x='Rainfall_Anomaly_mm', y='Reported_Confirmed_Cases', hue='Province', style='Province', s=100, ax=ax5)
    ax5.set_title("Rainfall Anomalies vs. Confirmed Infections")
    ax5.set_xlabel("Rainfall Anomaly (mm)")
    ax5.set_ylabel("Confirmed Cases")
    charts['scatter'] = fig5

    # 6. Box Plot (Plasmodium Vivax percentage distribution by Province)
    fig6, ax6 = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=df, x='Province', y='Plasmodium_Vivax_Pct', palette='Set3', hue='Province', legend=False, ax=ax6)
    ax6.set_title("Data Spread: Plasmodium Vivax Strain Proportion")
    ax6.set_ylabel("Vivax Strain Percentage (%)")
    charts['box'] = fig6

    # 7. Heatmap (Correlation matrix of features)
    fig7, ax7 = plt.subplots(figsize=(6, 4))
    numeric_cols =
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax7)
    ax7.set_title("Feature Correlation Matrix")
    charts['heatmap'] = fig7

    # 8. Area Chart (Cumulative trends over time)
    fig8, ax8 = plt.subplots(figsize=(6, 4))
    pivot_df = df.pivot_table(index='Year', columns='Province', values='Reported_Confirmed_Cases', aggfunc='sum').fillna(0)
    pivot_df.plot(kind='area', stacked=True, alpha=0.7, ax=ax8, color=sns.color_palette('Set2'))
    ax8.set_title("Cumulative Confirmed Case Burden Trend")
    ax8.set_ylabel("Cumulative Cases")
    charts['area'] = fig8

    # 9. Count Plot (Frequency count of data records per Province)
    fig9, ax9 = plt.subplots(figsize=(6, 4))
    sns.countplot(data=df, x='Province', palette='pastel', hue='Province', legend=False, ax=ax9)
    ax9.set_title("Data Tracking Frequency Count per Province")
    ax9.set_ylabel("Total Recorded Submissions")
    charts['count'] = fig9

    # 10. Violin Plot (Distribution and probability density of estimated deaths)
    fig10, ax10 = plt.subplots(figsize=(6, 4))
    sns.violinplot(data=df, x='Province', y='Estimated_Deaths_WHO', palette='light:g', hue='Province', legend=False, ax=ax10)
    ax10.set_title("Probability Density Spread of Estimated Deaths")
    ax10.set_ylabel("WHO Estimated Deaths")
    charts['violin'] = fig10

    return charts
