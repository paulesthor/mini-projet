import pandas as pd
import os

def extract(filepath):
    """
    Reads a CSV file and returns a pandas DataFrame.
    Verifies file existence and prints the number of rows extracted.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    try:
        df = pd.read_csv(filepath)
        print(f"Extracted {len(df)} rows from {filepath}")
        return df
    except Exception as e:
        raise Exception(f"Error reading {filepath}: {e}")
