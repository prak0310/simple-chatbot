from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

password = quote_plus("Pr@k031005##")  # Replace with your actual MySQL password

DATABASE_URL = f"mysql+pymysql://root:{password}@localhost/chatbot_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

