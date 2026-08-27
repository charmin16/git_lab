from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import jwt
from pwdlib import PasswordHash
from datetime import datetime, date, timedelta
from dotenv import load_dotenv
import os
from models import User

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


# get_current_user
def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(400, "Invalid credentials")
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


def get_admin(admin: User = Depends(get_current_user)):
    if admin.designation != "admin":
        raise HTTPException(403, detail="Only Admins Can Do This")
