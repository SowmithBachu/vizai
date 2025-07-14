import pandas as pd
import numpy as np

def clean_data(df):
    df.columns = df.columns.str.strip()
    df.dropna(axis=0, how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    for col in df.select_dtypes(include=[np.number]).columns:
        median_value = df[col].median()
        df[col].fillna(median_value, inplace=True)
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].isnull().any():
            try:
                mode_val = df[col].mode()[0]
                df[col].fillna(mode_val, inplace=True)
            except:
                df[col].fillna("Unknown", inplace=True)
    return df