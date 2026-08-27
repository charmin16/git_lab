from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import jwt
from pwdlib import PasswordHash
from datetime import datetime, date, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

password_hasher = PasswordHash.recommended()
oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

ACCESS_TOKEN_EXPIRY = 400
ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")


# create hashed password
def hash_password(password: str):
    return password_hasher.hash(password)


# verify hashed password
def verify_hashed_pwd(hashed: str, plain: str):
    return password_hasher.verify(plain, hashed)


# create token
def create_token(data: dict):
    to_encode = data.copy()

    to_encode.update({"expiry": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY)})

    jwt_encoded = jwt.encode(
        to_encode,
        SECRET_KEY,
        ALGORITHM=ALGORITHM
    )

    return jwt_encoded





