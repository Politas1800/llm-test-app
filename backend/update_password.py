from backend.models import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from backend.app import get_password_hash, verify_password

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()
user = db.query(User).filter(User.username == 'creator_user').first()

if user:
    new_password = "password123"
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.commit()
    print(f'Password updated for user: {user.username}')
    print(f'New hashed password: {user.hashed_password}')
    print(f'Password verification result: {verify_password(new_password, user.hashed_password)}')
else:
    print('User not found')

db.close()
