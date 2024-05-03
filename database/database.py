from mysql.connector import connect, pooling
from config import load_config
import logging

# Set up logging configuration to show information-level messages.
logging.basicConfig(level=logging.INFO)

# Initialize a global variable for the connection pool.
pool = None


def init_connection_pool():
    global pool  # Access the global pool variable
    try:
        config = load_config()  # Load database configuration
        if not config:
            # Log an error if the configuration is missing or empty
            logging.error("Configuration is empty or could not be loaded.")
            return
        # Create a new connection pool with settings from the configuration file
        pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=10,
            pool_reset_session=True,
            host=config["host"],
            user=config["user"],
            password=config["password"],
            charset="utf8mb4",
        )
    except Exception as e:
        # Raise an exception if pool initialization fails
        raise Exception(f"Failed to initialize connection pool: {e}")


def get_db_connection(database=None):
    try:
        # Get a connection from the pool
        conn = pool.get_connection()
        if database:
            # Switch to a different database if specified
            conn.cmd_query(f"USE {database}")
        return conn
    except Exception as e:
        # Log any errors that occur when establishing a database connection
        logging.error(f"Failed to establish database connection: {e}")
        return None


def execute_query(query, params=None, fetch=False, commit=False, database=None):
    # Obtain a database connection
    conn = get_db_connection(database=database)
    if conn is None:
        # Return None if the connection could not be established
        return None
    try:
        cursor = conn.cursor()  # Create a cursor object
        cursor.execute(query, params)  # Execute the SQL query
        if fetch:
            # Fetch and return results if fetch=True
            result = cursor.fetchall()
            return result
        if commit:
            # Commit the transaction if commit=True
            conn.commit()
    except Exception as e:
        # Log any errors during query execution and rollback the transaction
        logging.error(f"An error occurred during query execution: {e}")
        conn.rollback()
    finally:
        # Always close the cursor and connection
        cursor.close()
        conn.close()
