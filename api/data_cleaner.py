import pandas as pd

def clean_data(df):
    # Fill missing values with column mean for numeric, mode for categorical
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            df[col].fillna(df[col].mean(), inplace=True)
        else:
            df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else '', inplace=True)
    # Remove duplicate rows
    df.drop_duplicates(inplace=True)
    # Standardize column names
    df.columns = [str(c).strip().replace(' ', '_').lower() for c in df.columns]
    return df 