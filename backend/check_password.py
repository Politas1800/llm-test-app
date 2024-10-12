from backend.models import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from backend.app import verify_password

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()
user = db.query(User).filter(User.username == 'creator_user').first()

if user:
    print(f'Username: {user.username}')
    print(f'Hashed Password: {user.hashed_password}')
    print(f'Password verification result: {verify_password("password123", user.hashed_password)}')
else:
    print('User not found')

db.close()
