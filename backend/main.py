from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from backend.app import SessionLocal, engine, get_db, get_password_hash, authenticate_user, create_access_token, get_current_user, User, Test, TestStatus
from backend.models import Base
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://astonishing-starburst-9b00b3.netlify.app"],  # Add your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

async def get_current_user_optional(token: Optional[str] = Depends(oauth2_scheme_optional)):
    if token:
        return await get_current_user(token)
    return None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TestCreate(BaseModel):
    title: str
    description: str
    user_message: str
    review_message: str
    num_requests: int
    selected_llms: List[str]

@app.post("/register", response_model=Token)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)

    # Check if this is the first user, if so, make them an Admin
    if db.query(User).count() == 0:
        new_user.role = "Admin"

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info(f"Login attempt for user: {form_data.username}")
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    logger.info(f"Successful login for user: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/tests")
async def create_test(test: TestCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["Creator", "Admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to create tests")
    db_test = Test(
        title=test.title,
        description=test.description,
        user_message=test.user_message,
        review_message=test.review_message,
        num_requests=test.num_requests,
        selected_llms=json.dumps(test.selected_llms),
        status=TestStatus.CREATED.value,
        results="{}",
        creator_id=current_user.id
    )
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

@app.get("/tests")
async def get_tests(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_optional)):
    if not current_user:
        return db.query(Test).filter(Test.published == True).all()
    elif current_user.role == "Admin":
        return db.query(Test).all()
    elif current_user.role == "Creator":
        return db.query(Test).filter(Test.creator_id == current_user.id).all()
    else:
        return db.query(Test).filter(Test.published == True).all()

async def get_current_user_optional(token: str = Depends(oauth2_scheme_optional)):
    if token:
        return await get_current_user(token)
    return None

oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

# Create tables
Base.metadata.create_all(bind=engine)
