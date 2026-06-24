from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User, Conversation, Message
from backend.schemas import UserCreate, UserLogin
from backend.auth import hash_password, verify_password
from backend.models import Base
from backend.database import engine
from fastapi.middleware.cors import CORSMiddleware

from backend.chatbot import get_ai_response
from fastapi.staticfiles import StaticFiles



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = User(
        username=user.username,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "User registered successfully"
    }


@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "message": "Login successful"
    }


@app.post("/chat")
def chat(data: dict, db: Session = Depends(get_db)):

    user_message = data["message"]

    db.add(
        Message(
            conversation_id=1,
            sender="user",
            content=user_message
        )
    )

    ai_response = get_ai_response(
        user_message
    )

    db.add(
        Message(
            conversation_id=1,
            sender="bot",
            content=ai_response
        )
    )

    db.commit()

    return {
        "response": ai_response
    }



@app.get("/chat-history")
def chat_history(db: Session = Depends(get_db)):

    messages = db.query(Message).filter(
        Message.conversation_id == 1
    ).all()

    return messages

    