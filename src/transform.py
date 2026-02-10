import pandas as pd
import numpy as np

def transform_players(df):
    """
    Cleans player data:
    1. Removes duplicates on player_id
    2. Trims whitespace from usernames
    3. Converts registration_date (coerces errors)
    4. Replaces invalid emails (missing @) with None
    """
    original_count = len(df)
    
    # 1. Remove duplicates on player_id
    df = df.drop_duplicates(subset=['player_id'], keep='first').copy()
    
    # 2. Strip whitespace from usernames
    if 'username' in df.columns:
        df['username'] = df['username'].str.strip()
    
    # 3. Convert registration_date
    if 'registration_date' in df.columns:
        df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')
    
    # 4. Replace invalid emails
    if 'email' in df.columns:
        # Use regex to identify valid emails, anything else becomes None (NaN)
        # Simple check for '@' as per requirements
        mask = df['email'].astype(str).str.contains('@')
        df.loc[~mask, 'email'] = None
        
        # Also handle empty strings or NaN explicitly if needed, but the mask handles non-matches
        df['email'] = df['email'].replace({np.nan: None})
        
    print(f"Transformed players: {original_count} -> {len(df)} rows")
    return df

def transform_scores(df, valid_player_ids):
    """
    Cleans score data:
    1. Removes duplicates on score_id
    2. Converts dates and scores to numeric/datetime
    3. Removes negative or zero scores
    4. Removes duplicates on (player_id, game), keeping highest score
    5. Removes scores with player_id not in valid_player_ids
    """
    original_count = len(df)
    
    # 1. Remove duplicates on score_id
    df = df.drop_duplicates(subset=['score_id'], keep='first').copy()
    
    # 2. Convert types
    if 'score' in df.columns:
        df['score'] = pd.to_numeric(df['score'], errors='coerce')
    
    if 'played_at' in df.columns:
        df['played_at'] = pd.to_datetime(df['played_at'], errors='coerce')
        
    if 'duration_minutes' in df.columns:
         df['duration_minutes'] = pd.to_numeric(df['duration_minutes'], errors='coerce')

    # 3. Remove negative or null scores (requirement says "negative or zero" - usually implying > 0)
    # Checking requirement: "Supprimer les lignes avec un score négatif ou nul" (negative or null/zero)
    # Note: NaN comparisons.
    df = df[df['score'] > 0]
    
    # Remove rows with invalid dates (NaT) -> CHANGED: NOW WE KEEP THEM AS NULL
    # df = df.dropna(subset=['played_at'])

    # 4. Remove duplicates on (player_id, game), keeping the highest score
    # Sort by score descending, then drop duplicates keeping first (highest)
    df = df.sort_values('score', ascending=False)
    df = df.drop_duplicates(subset=['player_id', 'game'], keep='first')

    # 5. Filter orphans
    # valid_player_ids should be a list or set
    df = df[df['player_id'].isin(valid_player_ids)]
    
    print(f"Transformed scores: {original_count} -> {len(df)} rows")
    return df
