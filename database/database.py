from mysql.connector import connect
from config import load_config
import logging

logging.basicConfig(level=logging.INFO)

def get_db_connection():
    try:
        config = load_config()
        conn = connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
            charset="utf8mb4"
        )
        print("Database connection established successfully to", config["database"])
        return conn
    except Exception as e:
        logging.error(f"Failed to establish database connection: {e}")
        return None

def execute_query(query, params=None, fetch=False, commit=False):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetch:
            result = cursor.fetchall()
            return result
        if commit:
            conn.commit()
    except Exception as e:
        logging.error(f"An error occurred during query execution: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")

