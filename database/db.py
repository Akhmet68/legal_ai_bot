import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

print("DB_NAME:", DB_NAME)
print("DB_USER:", DB_USER)
print("DB_PASSWORD is set:", bool(DB_PASSWORD))
print("DB_HOST:", DB_HOST)
print("DB_PORT:", DB_PORT)


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

    # Таблица клиентов
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

    # Таблица дел (кейсы)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cases (
            id SERIAL PRIMARY KEY,
            tg_id BIGINT,
            type TEXT,
            summary TEXT,
            pdf_path TEXT,
            status TEXT DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    conn.commit()
    conn.close()
