import pandas as pd

def load_and_clean_data(filepath):
    """
    Loads the malaria dataset and ensures all column names and data types are clean.
    """
    try:
        df = pd.read_csv(filepath)
        # Strip any accidental whitespaces from column names
        df.columns = df.columns.str.strip()
        
        # Ensure numerical types are correct
        df = df.astype(int)
        df = df.astype(int)
        df = df.astype(int)
        df = df.astype(int)
        df = df.astype(int)
        
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def apply_dashboard_filters(df, selected_provinces, year_range, rainfall_range):
    """
    Applies the active dashboard sidebar selections to dynamically filter rows.
    """
    if df.empty:
        return df
        
    # 1. Category Filter (Multi-Select)
    if selected_provinces:
        df = df[df['Province'].isin(selected_provinces)]
        
    # 2. Numerical Range Filter (Year Slider)
    df = df >= year_range) & (df <= year_range[1])]
    
    # 3. Numerical Range Filter (Rainfall Slider)
    df = df >= rainfall_range) & (df <= rainfall_range[1])]
    
    return df
