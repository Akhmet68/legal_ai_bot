import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("postgres")
DB_USER = os.getenv("postgres")
DB_PASSWORD = os.getenv("1234")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )


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
        )
        """
    )

    conn.commit()
    conn.close()
