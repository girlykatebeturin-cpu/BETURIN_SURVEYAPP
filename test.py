from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from database import create_db_and_tables, engine
from fastapi.middleware.cors import CORSMiddleware
from models import Survey, User

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
async def register_user(user: User):
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.username == user.username)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"status": "success", "message": "User registered"}

@app.post("/login")
async def login_user(user: User):
    with Session(engine) as session:
        db_user = session.exec(
            select(User).where(User.username == user.username, User.password == user.password)
        ).first()
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        return {"status": "success", "username": db_user.username}

@app.post("/Survey")
async def create_Survey(survey: Survey):
    with Session(engine) as session:
        session.add(survey)
        session.commit()
        session.refresh(survey)
        return {"status": "success", "message": survey}

@app.get("/Survey/user/{username}")
async def read_user_survey(username: str):
    with Session(engine) as session:
        # Gets the most recent survey submitted by this user
        survey = session.exec(
            select(Survey).where(Survey.username == username).order_by(Survey.id.desc())
        ).first()
        if not survey:
            raise HTTPException(status_code=404, detail="No survey found for this user")
        return {"status": "success", "data": survey}