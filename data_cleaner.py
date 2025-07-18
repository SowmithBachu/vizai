import pandas as pd
import numpy as np

def clean_data(df):
    df.columns = df.columns.str.strip()
    df.dropna(axis=0, how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    for col in df.select_dtypes(include=[np.number]).columns:
        median_value = df[col].median()
        # Avoid chained assignment warning
        df[col] = df[col].fillna(median_value)
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].isnull().any():
            try:
                mode_val = df[col].mode()[0]
                df[col] = df[col].fillna(mode_val)
            except:
                df[col] = df[col].fillna("Unknown")
    return df