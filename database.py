from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3

DB_URL = "sqlite:///nexa.db"

engine = create_engine(DB_URL, connect_args={"create_same_thread": False})

SessionLocal = sessionmaker(autoflush=False, autocommit=True, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

