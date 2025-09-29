import psycopg2
import logging
import os

conn = None

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

def get_conn():
    global conn
    if conn is None:
        DBHOST = os.getenv("DBHOST")
        DB = os.getenv("DB")
        DBUSER = os.getenv("DBUSER")
        DBPASSWORD = os.getenv("DBPASSWORD")
        DBPORT = os.getenv("DBPORT")
        # print(DBHOST, DB, DBUSER, DBPASSWORD, DBPORT)
        logging.info("DBHOST: %s, DB: %s, DBUSER: %s, DBPASSWORD: %s, DBPORT: %s", DBHOST, DB, DBUSER, DBPASSWORD, DBPORT)
        conn = connect_db(host=DBHOST, database=DB, user=DBUSER, password=DBPASSWORD, port=DBPORT)
    return conn