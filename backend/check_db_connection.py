from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
print(f'Database URL: {DATABASE_URL}')

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print('Successfully connected to the database')
    connection.close()
except Exception as e:
    print(f'Failed to connect to the database: {str(e)}')
