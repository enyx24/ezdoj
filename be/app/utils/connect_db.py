import psycopg2
import logging

def connect_db(host="localhost", database="postgres", user="postgres", password="123456", port=5432):
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        logging.info("Connection established")
        return conn
    except Exception as e:
        logging.error("Connection failed: %s", e)
        return None

def close_db(conn):
    if conn:
        conn.close()
        logging.info("Connection closed")