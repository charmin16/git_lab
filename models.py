from sqlalchemy import (Column, String, ForeignKey, Float, Integer, Date,
                        Enum as SQLEnum, Numeric, Boolean, DateTime)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from datetime import datetime, date
from enums import UserRole, ListingType, PropertyStatus

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(12), nullable=False)
    display_name = Column(String(100), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    created_at = Column(Date, default=date.today)

    properties = relationship(
        "Property",
        back_populates="user"
    )


class Property(Base):
    __tablename__ = "property"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    area = Column(String(100), nullable=False)
    bedrooms = Column(Integer, nullable=True)
    listing = Column(SQLEnum(ListingType))
    status = Column(SQLEnum(PropertyStatus), default=PropertyStatus.APPROVED)
    price = Column(Numeric(3, 2), nullable=True)
    annual_rent = Column(Numeric(3, 2), nullable=True)
    lawyer_fee = Column(Numeric(3, 2), nullable=True)
    caution_fee = Column(Numeric(3, 2), nullable=True)
    has_c_of_o = Column(Boolean, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))

    user = relationship(
        "User",
        back_populates="properties"
    )

    prop_media = relationship(
        "PropertyMedia",
        back_populates="property"
    )


class PropertyMedia(Base):
    __tablename__ = "property_media"
    id = Column(Integer, primary_key=True)
    filename = Column(String(200), nullable=True)
    filepath = Column(String(200), nullable=True)
    media_type = Column(String(50), nullable=True)

    property_id = Column(Integer, ForeignKey("property.id"))

    property = relationship(
        "Property",
        back_populates="prop_media"
    )


class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


