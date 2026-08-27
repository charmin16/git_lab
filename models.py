from sqlalchemy import Column, String, ForeignKey, Float, Integer, Date
from sqlalchemy.orm import declarative_base
from datetime import datetime, date

Base = declarative_base()


class User(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(100), nullable=False)
    created_at = Column(Date, default=date.today)