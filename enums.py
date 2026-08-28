from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    LANDLORD = "landlord"
    SELLER = "seller"


class ListingType(str, Enum):
    RENT = "rent"
    SALE = "sale"


class PropertyStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    RENTED = "rented"
    SOLD = "sold"
