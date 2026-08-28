from sqlalchemy import (Column, String, ForeignKey, Float, Integer, Date,
                        Enum as SQLEnum, Numeric, Boolean, DateTime)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from datetime import datetime, date
from enums import UserRole, ListingType

Base = declarative_base()


class User(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(100), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    created_at = Column(Date, default=date.today)

    properties = relationship(
        "User",
        back_populates="user"
    )


class Property(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    area = Column(String(100), nullable=False)
    bedrooms = Column(Integer, nullable=False)
    listing = Column(SQLEnum(ListingType))
    price = Column(Numeric(3, 2), nullable=False)
    annual_rent = Column(Numeric(3, 2), nullable=False)
    lawyer_fee = Column(Numeric(3, 2), nullable=False)
    caution_fee = Column(Numeric(3, 2), nullable=False)
    has_c_of_o = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))

    users = relationship(
        "User",
        back_populates="properties"
    )


