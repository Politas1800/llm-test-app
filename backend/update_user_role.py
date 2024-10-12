from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import User
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()
user = db.query(User).filter(User.username == 'creator_user').first()
if user:
    user.role = "Creator"
    db.commit()
    print(f'Updated {user.username} role to {user.role}')
else:
    print('User not found')
db.close()
