import streamlit as st
import os
from filters import load_and_clean_data, apply_dashboard_filters
from charts import generate_all_charts

# Page Settings
st.set_page_config(page_title="Pakistan Malaria Dashboard", layout="wide", page_icon="📊")

# Header Block
st.title("📊 Malaria Epidemiological Dashboard — Pakistan")
st.markdown("An interactive platform tracking data-driven trends, mortality anomalies, and vector interventions.")
st.markdown("---")

# File Resolution Strategy
DATA_FILE = "data/malaria_data.csv"

if not os.path.exists(DATA_FILE):
    st.error(f"🚨 Critical Failure: '{DATA_FILE}' not found! Please place the CSV file inside the 'data' folder.")
    st.stop()

raw_data = load_and_clean_data(DATA_FILE)

if raw_data.empty:
    st.error("🚨 Failed to load data. Please check if the CSV file content is formatted correctly.")
    st.stop()

# Sidebar Navigation Framework
st.sidebar.header("🎛️ Interactive Controls")

# Category Filtering Setup
provinces_available = raw_data['Province'].unique().tolist()
selected_provinces = st.sidebar.multiselect("Filter by Provinces", provinces_available, default=provinces_available)

# Numerical Range Framework (Year & Rainfall Sliders)
min_y, max_y = int(raw_data.min()), int(raw_data.max())
year_range = st.sidebar.slider("Select Timeline Boundaries", min_y, max_y, (min_y, max_y))

min_r, max_r = float(raw_data.min()), float(raw_data.max())
rainfall_range = st.sidebar.slider("Rainfall Anomaly Window (mm)", min_r, max_r, (min_r, max_r))

# Master Reset Implementation
if st.sidebar.button("Reset / Clear Filters", use_container_width=True):
    st.rerun()

# Apply Interactive Pipeline Data
filtered_data = apply_dashboard_filters(raw_data, selected_provinces, year_range, rainfall_range)

# Primary KPI Metric Interface Display
kpi_total_records = len(filtered_data)
kpi_confirmed_cases = filtered_data.sum() if kpi_total_records > 0 else 0
kpi_estimated_deaths = filtered_data.sum() if kpi_total_records > 0 else 0

metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    st.metric(label="Total Logged Profiles", value=f"{kpi_total_records}")
with metric_col2:
    st.metric(label="Aggregated Confirmed Cases", value=f"{kpi_confirmed_cases:,}")
with metric_col3:
    st.metric(label="WHO Modeled Deaths (Est.)", value=f"{kpi_estimated_deaths:,}")

st.markdown("---")

# Connected Graphics Display Section (10 Linked Charts)
if not filtered_data.empty:
    chart_objects = generate_all_charts(filtered_data)
    
    # Row 1
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(chart_objects['line'])
    with col2:
        st.pyplot(chart_objects['pie'])
        
    st.markdown("---")
    
    # Row 2
    col3, col4 = st.columns(2)
    with col3:
        st.pyplot(chart_objects['bar'])
    with col4:
        st.pyplot(chart_objects['scatter'])

    st.markdown("---")
    
    # Row 3
    col5, col6 = st.columns(2)
    with col5:
        st.pyplot(chart_objects['area'])
    with col6:
        st.pyplot(chart_objects['box'])

    st.markdown("---")
    
    # Row 4
    col7, col8 = st.columns(2)
    with col7:
        st.pyplot(chart_objects['hist'])
    with col8:
        st.pyplot(chart_objects['heatmap'])

    st.markdown("---")
    
    # Row 5
    col9, col10 = st.columns(2)
    with col9:
        st.pyplot(chart_objects['count'])
    with col10:
        st.pyplot(chart_objects['violin'])
else:
    st.warning("⚠️ No records match the selected criteria. Adjust your sidebar sliders.")
