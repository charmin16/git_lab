from fastapi import (FastAPI, Depends, HTTPException, File, Form,
                     UploadFile, status)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models import User, Property, PropertyMedia, Base
from database import get_db, engine
from security import hash_password, verify_hashed_pwd, create_token, get_current_user, get_admin
from schema import CreateProperty, CreateUser
from file_services import verify_photo
from datetime import datetime, date
from typing import Annotated

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
@app.post("/login")
def login_user(formdata: OAuth2PasswordRequestForm = Depends(),
               db: Session = Depends(get_db)):
    existing = db.query(User).filter_by(username=formdata.username).first()

    if not existing:
        raise HTTPException(404, "Invalid username or password")

    if not verify_hashed_pwd(existing.password_hash, formdata.password):
        raise HTTPException(404, "Invalid username or password")

    access_token = create_token({"sub": str(existing.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# create property
@app.post("/property")
def create_property(
        prop: Annotated[CreateProperty, Form()],
        media: list[UploadFile] | None = File(None),
        db: Session = Depends(get_db)):

    new_prop = Property(title=prop.title,
                        city=prop.city,
                        area=prop.area,
                        bedrooms=prop.bedrooms,
                        listing=prop.listing,
                        price=prop.price,
                        annual_rent=prop.annual_rent,
                        lawyer_fee=prop.lawyer_fee,
                        caution_fee=prop.caution_fee,
                        has_c_of_o=prop.has_c_of_o)

    db.add(new_prop)
    db.flush()

    for med in media:
        media_file = verify_photo(med)
        new_media = PropertyMedia(
            filename=media_file.filename,
            filepath=media_file.filepath,
            media_type=media_file.media_type,
            property_id=new_prop.id
        )

        db.add(new_media)

    db.commit()

    return {"msg": f"{prop.title} and its media files added successfully"}




