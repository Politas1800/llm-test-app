import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
print(f'Database URL: {DATABASE_URL}')

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("Connected to the database successfully")
    cur = conn.cursor()
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    print(f"PostgreSQL database version: {db_version}")
    cur.close()
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if conn:
        conn.close()
        print("PostgreSQL connection is closed")
