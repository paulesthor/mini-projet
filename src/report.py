import os
from src.database import database_connection
from datetime import datetime

def generate_report():
    """
    Generates a summary report from the database.
    """
    report_path = '/app/output/rapport.txt'
    
    queries = {
        "stats_general": """
            SELECT 
                (SELECT COUNT(*) FROM players) as nb_players,
                (SELECT COUNT(*) FROM scores) as nb_scores,
                (SELECT COUNT(DISTINCT game) FROM scores) as nb_games
        """,
        "top_5": """
            SELECT p.username, s.game, s.score
            FROM scores s
            JOIN players p ON s.player_id = p.player_id
            ORDER BY s.score DESC
            LIMIT 5
        """,
        "avg_score": """
            SELECT game, AVG(score) as avg_score
            FROM scores
            GROUP BY game
        """,
        "players_by_country": """
            SELECT country, COUNT(*) as count
            FROM players
            GROUP BY country
            ORDER BY count DESC
        """,
        "sessions_by_platform": """
            SELECT platform, COUNT(*) as count
            FROM scores
            GROUP BY platform
            ORDER BY count DESC
        """
    }
    
    try:
        with database_connection() as conn:
            cursor = conn.cursor()
            
            # Execute queries
            results = {}
            for key, query in queries.items():
                cursor.execute(query)
                results[key] = cursor.fetchall()
                
            # Write report
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =\n")
                f.write("G A M E T R A C K E R - Rapport de synthèse\n")
                f.write(f"Généré le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =\n")
                
                # General Stats
                stats = results['stats_general'][0]
                f.write("--- Statistiques générales ---\n")
                f.write(f"Nombre de joueurs : {stats[0]}\n")
                f.write(f"Nombre de scores : {stats[1]}\n")
                f.write(f"Nombre de jeux : {stats[2]}\n")
                
                # Top 5
                f.write("--- Top 5 des meilleurs scores ---\n")
                for i, row in enumerate(results['top_5']):
                    f.write(f"{i+1}. {row[0]} | {row[1]} | {row[2]}\n")
                    
                # Avg Score
                f.write("--- Score moyen par jeu ---\n")
                for row in results['avg_score']:
                    f.write(f"{row[0]} : {row[1]:.1f}\n")
                    
                # Players by Country
                f.write("--- Joueurs par pays ---\n")
                for row in results['players_by_country']:
                    f.write(f"{row[0]} : {row[1]}\n")
                    
                # Sessions by Platform
                f.write("--- Sessions par plateforme ---\n")
                for row in results['sessions_by_platform']:
                    f.write(f"{row[0]} : {row[1]}\n")
                    
        print(f"Report generated successfully at {report_path}")
        
    except Exception as e:
        print(f"Error generating report: {e}")
        raise e
