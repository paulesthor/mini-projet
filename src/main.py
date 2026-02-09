import sys
import os

# Ensure src is in path if running as script
sys.path.append('/app')

from src.extract import extract
from src.transform import transform_players, transform_scores
from src.load import load_players, load_scores
from src.database import database_connection
from src.report import generate_report

def main():
    print("--- Starting GameTracker Pipeline ---")
    
    try:
        # Define paths
        data_dir = '/app/data/raw'
        players_path = os.path.join(data_dir, 'Players.csv')
        scores_path = os.path.join(data_dir, 'Scores.csv')
        
        # 1. Extract
        print("[1/4] Extracting data...")
        df_players = extract(players_path)
        df_scores = extract(scores_path)
        
        # 2. Transform
        print("[2/4] Transforming data...")
        # Transform players first to get valid IDs
        df_players_clean = transform_players(df_players)
        valid_player_ids = df_players_clean['player_id'].unique()
        
        # Transform scores using valid IDs
        df_scores_clean = transform_scores(df_scores, valid_player_ids)
        
        # 3. Load
        print("[3/4] Loading data into database...")
        with database_connection() as conn:
            load_players(df_players_clean, conn)
            load_scores(df_scores_clean, conn)
            
        # 4. Report
        print("[4/4] Generating report...")
        generate_report()
        
        print("--- Pipeline Finished Successfully ---")
        
    except Exception as e:
        print(f"CRITICAL ERROR: Pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
