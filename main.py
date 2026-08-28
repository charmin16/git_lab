from fastapi import (FastAPI, Depends, HTTPException, File, Form,
                     UploadFile, status)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models import User, Property, PropertyMedia, Base
from database import get_db, engine
from security import hash_password, verify_hashed_pwd, create_token, get_current_user, get_admin
from schema import CreateProperty, CreateUser
from datetime import datetime, date

# configurations
app = FastAPI()


# create user
@app.post("/user")
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=user.username).first():
        raise HTTPException(409, f"{user.username} already exists")
    pwd_hash = hash_password(user.password)

    new_user = User(username=user.username, password_hash=pwd_hash, phone=user.phone, display_name=user.display_name,
                    role=user.role)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": f"{user.username} added successfully"}


# login user
