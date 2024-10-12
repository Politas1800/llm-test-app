from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from enum import Enum
import json
import asyncio
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

load_dotenv()

load_dotenv()

app = FastAPI()

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

# Database setup
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/dbname")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password hashing and JWT setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="Viewer")

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserInDB(BaseModel):
    id: int
    username: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class TestStatus(str, Enum):
    CREATED = "Created"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"

class TestRequest(BaseModel):
    title: str
    description: str
    user_message: str
    review_message: str
    num_requests: int
    selected_llms: List[str]

class TestResponse(BaseModel):
    id: int
    title: str
    description: str
    user_message: str
    review_message: str
    num_requests: int
    selected_llms: List[str]
    status: TestStatus
    created_at: datetime
    creator_id: int

    model_config = ConfigDict(from_attributes=True)

# Add Test model for database
class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    user_message = Column(String)
    review_message = Column(String)
    num_requests = Column(Integer)
    selected_llms = Column(String)  # Store as JSON string
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    creator_id = Column(Integer, ForeignKey("users.id"))

# Authentication functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User registration endpoint
@app.post("/register", response_model=UserInDB)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)

    # Check if this is the first user, if so, make them an Admin
    if db.query(User).count() == 0:
        new_user = User(username=user.username, email=user.email, hashed_password=hashed_password, role="Admin")
    else:
        new_user = User(username=user.username, email=user.email, hashed_password=hashed_password, role="Creator")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Token generation endpoint
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/tests", response_model=TestResponse)
async def create_test(test_request: TestRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role not in ["Creator", "Admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to create tests")

    new_test = Test(
        title=test_request.title,
        description=test_request.description,
        user_message=test_request.user_message,
        review_message=test_request.review_message,
        num_requests=test_request.num_requests,
        selected_llms=json.dumps(test_request.selected_llms),
        status=TestStatus.CREATED.value,
        creator_id=current_user.id
    )
    db.add(new_test)
    db.commit()
    db.refresh(new_test)

    asyncio.create_task(run_test(new_test.id, test_request, db))

    return TestResponse.model_validate({**new_test.__dict__, 'selected_llms': json.loads(new_test.selected_llms)})

# Update get_tests endpoint
@app.get("/tests", response_model=List[TestResponse])
async def get_tests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role not in ["Creator", "Admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to view tests")
    tests = db.query(Test).filter(Test.creator_id == current_user.id).all()
    return [TestResponse.model_validate({**test.__dict__, 'selected_llms': json.loads(test.selected_llms)}) for test in tests]

# Update get_test endpoint
@app.get("/tests/{test_id}", response_model=TestResponse)
async def get_test(test_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role not in ["Creator", "Admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to view tests")

    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    return TestResponse.from_orm(test)

# Update run_test function
async def run_test(test_id: int, test_request: TestRequest, db: Session):
    test = db.query(Test).filter(Test.id == test_id).first()
    test.status = TestStatus.RUNNING.value
    db.commit()

    try:
        for llm in test_request.selected_llms:
            llm_results = []
            for _ in range(test_request.num_requests):
                response = await run_anthropic_request(test_request.user_message, llm)
                review = await run_anthropic_review(response, test_request.review_message)
                llm_results.append({"response": response, "review": review})
            test.results = json.dumps({**json.loads(test.results), llm: llm_results})
            db.commit()
        test.status = TestStatus.COMPLETED.value
    except Exception as e:
        test.status = TestStatus.FAILED.value
        print(f"Error in run_test: {str(e)}")

    db.commit()

async def run_anthropic_request(message: str, model: str, max_retries=3):
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "Content-Type": "application/json",
                        "X-API-Key": ANTHROPIC_API_KEY,
                        "anthropic-version": "2023-06-01"
                    },
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": message}],
                        "max_tokens": 1000,
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()["content"][0]["text"]
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:  # Rate limit error
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limit reached. Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                print(f"HTTP error occurred: {e}")
                if attempt == max_retries - 1:
                    raise
        except Exception as e:
            print(f"An error occurred: {e}")
            if attempt == max_retries - 1:
                raise
    raise Exception("Max retries reached. Unable to complete the request.")

async def run_anthropic_review(llm_response: str, review_instructions: str):
    review_prompt = f"""—FIRST_LLM_MESSAGE— Here is the answer I got from an LLM:

```
{llm_response}
```

I want you to tell me if the answer above is correct. Here are the instructions that say what should be the correct answer:

```
{review_instructions}
```

Now, respond only with **ONE** word that can be either `TRUE` (if the answer from the LLM matches instructions provided) or `FALSE` (if the answer from the LLM doesn't match the instructions provided). —END_OF_FIRST_LLM_MESSAGE—"""

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "X-API-Key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-3-5-sonnet-20240620",
                "messages": [{"role": "user", "content": review_prompt}],
                "max_tokens": 1,
                "temperature": 0,
            },
        )
        response.raise_for_status()
        return response.json()["content"][0]["text"].strip()

@app.websocket("/ws/{test_id}")
async def websocket_endpoint(websocket: WebSocket, test_id: int, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            test = db.query(Test).filter(Test.id == test_id).first()
            if test:
                await websocket.send_json({
                    "status": test.status,
                    "results": json.loads(test.results)
                })
                if test.status in [TestStatus.COMPLETED.value, TestStatus.FAILED.value]:
                    break
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
    finally:
        await websocket.close()

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

# Add this new endpoint to change user roles
@app.put("/users/{user_id}/role", response_model=UserInDB)
async def change_user_role(user_id: int, new_role: str = Body(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Not authorized to change user roles")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if new_role not in ["Viewer", "Creator", "Admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    user.role = new_role
    db.commit()
    db.refresh(user)
    return user
