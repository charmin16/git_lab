from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import jwt
from pwdlib import PasswordHash
from datetime import datetime, date, timedelta

password_hasher = PasswordHash.recommended()
oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")


# create hashed password
def hash_password(password: str):
    return password_hasher.hash(password)


# verify hashed password
def verify_hashed_pwd(hashed: str, plain: str):
    return password_hasher.verify(plain, hashed)



