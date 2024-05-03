from mysql.connector import connect, pooling
from config import load_config
import logging

logging.basicConfig(level=logging.INFO)


pool = None


def init_connection_pool():
    global pool
    try:


        config = load_config()
        if not config:
            logging.error("Configuration is empty or could not be loaded.")
            return
        pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=10,
            pool_reset_session=True,
            host=config["host"],
            user=config["user"],
            password=config["password"],
            charset="utf8mb4"
        )
        logging.info("Connection pool was successfully initialized.")
        logging.info(f"Connection pool initialized with object: {pool}")
    except Exception as e:
        logging.error(f"Failed to initialize the connection pool: {e}")
        raise  # This will cause the application to exit if the pool cannot be initialized.




def get_db_connection(database=None):
    try:
        conn = pool.get_connection()
        if database:
            conn.cmd_query(f"USE {database}")
        return conn
    except Exception as e:
        logging.error(f"Failed to establish database connection: {e}")
        return None



def execute_query(query, params=None, fetch=False, commit=False, database=None):
    conn = get_db_connection(database=database)
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
