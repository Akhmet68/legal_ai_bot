import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")


def get_connection():
    conn = psycopg2.connect(
        host=5432,
        port=5432,
        dbname=postgres,
        user=postgres,
        password=1234
    )
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            tg_id BIGINT,
            name TEXT,
            phone TEXT,
            notes TEXT
        );
        """
    )

    conn.commit()
    conn.close()
