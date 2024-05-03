from mysql.connector import connect
from config import load_config
import logging

def test_db_connection():
    try:
        config = load_config()
        conn = connect(
            host=config["host"],
            user=config["user"],
            password=config["password"]
        )
        print("Successfully connected to the database.")
        conn.close()
    except Exception as e:
        print(f"Failed to connect to the database: {e}")

if __name__ == "__main__":
    test_db_connection()
