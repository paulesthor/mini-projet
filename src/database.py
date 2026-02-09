import mysql.connector
from mysql.connector import Error
from .config import Config
import time
from contextlib import contextmanager

def get_connection():
    """Establishes a connection to the database."""
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            port=Config.DB_PORT
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def get_connection_with_retry(max_retries=5, delay=2):
    """Establishes a connection with retry logic."""
    for attempt in range(max_retries):
        conn = get_connection()
        if conn is not None:
            return conn
        print(f"Connection failed (attempt {attempt + 1}/{max_retries}). Retrying in {delay}s...")
        time.sleep(delay)
    raise Exception("Could not connect to the database after multiple attempts.")

@contextmanager
def database_connection():
    """Context manager for database connections."""
    connection = None
    try:
        connection = get_connection_with_retry()
        yield connection
        connection.commit()
    except Exception as e:
        if connection:
            connection.rollback()
        raise e
    finally:
        if connection and connection.is_connected():
            connection.close()
