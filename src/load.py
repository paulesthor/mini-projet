import mysql.connector
import pandas as pd

def load_players(df, conn):
    """
    Inserts players into the database.
    Uses ON DUPLICATE KEY UPDATE.
    """
    cursor = conn.cursor()
    query = """
    INSERT INTO players (player_id, username, email, registration_date, country, level)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        username = VALUES(username),
        email = VALUES(email),
        registration_date = VALUES(registration_date),
        country = VALUES(country),
        level = VALUES(level)
    """
    
    data = []
    for _, row in df.iterrows():
        # Convert pandas NaN/None to None for SQL
        # Registration date: convert to string 'YYYY-MM-DD' or None
        reg_date = row['registration_date']
        if pd.isna(reg_date):
            reg_date = None
        else:
            reg_date = reg_date.strftime('%Y-%m-%d')
            
        data.append((
            row['player_id'],
            row['username'],
            row['email'],
            reg_date,
            row['country'],
            row['level']
        ))
        
    try:
        cursor.executemany(query, data)
        conn.commit()
        print(f"Loaded {cursor.rowcount} players (inserted/updated).")
    except mysql.connector.Error as e:
        print(f"Error loading players: {e}")
        conn.rollback()
    finally:
        cursor.close()

def load_scores(df, conn):
    """
    Inserts scores into the database.
    Uses ON DUPLICATE KEY UPDATE.
    """
    cursor = conn.cursor()
    query = """
    INSERT INTO scores (score_id, player_id, game, score, duration_minutes, played_at, platform)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        player_id = VALUES(player_id),
        game = VALUES(game),
        score = VALUES(score),
        duration_minutes = VALUES(duration_minutes),
        played_at = VALUES(played_at),
        platform = VALUES(platform)
    """
    
    data = []
    for _, row in df.iterrows():
        # Handle datetime
        played_at = row['played_at']
        if pd.isna(played_at):
            played_at = None
        else:
            played_at = played_at.strftime('%Y-%m-%d %H:%M:%S')

        data.append((
            row['score_id'],
            row['player_id'],
            row['game'],
            row['score'],
            row['duration_minutes'],
            played_at,
            row['platform']
        ))
        
    try:
        cursor.executemany(query, data)
        conn.commit()
        print(f"Loaded {cursor.rowcount} scores (inserted/updated).")
    except mysql.connector.Error as e:
        print(f"Error loading scores: {e}")
        conn.rollback()
    finally:
        cursor.close()
