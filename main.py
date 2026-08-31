from fastapi import (FastAPI, Depends, HTTPException, File, Form,
                     UploadFile, status)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models import User, Property, PropertyMedia, Base
from database import get_db, engine
from security import hash_password, verify_hashed_pwd, create_token, get_current_user, get_admin
from schema import CreateProperty, CreateUser, UpdateProp, PropNotAvail
from file_services import verify_photo
from datetime import datetime, date
from typing import Annotated
from enums import PropertyStatus, UserRole, ListingType
from math import ceil

# configurations
app = FastAPI()


# create user
@app.post("/user")
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=user.username).first():
        raise HTTPException(409, f"{user.username} already exists")
    pwd_hash = hash_password(user.password)

    new_user = User(username=user.username, password_hash=pwd_hash, phone=user.phone, display_name=user.display_name)

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


'''@app.post("/properties")
def create_property(
    title: str = Form(...),
):
    return {"title": title}
'''


# create property
@app.post("/properties")
def create_property(
        # prop: Annotated[CreateProperty, Form(...)],
        title: str = Form(...),
        city: str = Form(...),
        area: str = Form(...),
        bedrooms: int | None = Form(None),
        listing: ListingType = Form(...),
        price: float | None = Form(None),
        annual_rent: float | None = Form(None),
        lawyer_fee: float | None = Form(None),
        caution_fee: float | None = Form(None),
        has_c_of_o: bool | None = Form(None),
        cur_user: User = Depends(get_current_user),
        media: list[UploadFile] | None = File(None),
        db: Session = Depends(get_db)):

    prop = CreateProperty(
        title=title,
        city=city,
        area=area,
        bedrooms=bedrooms,
        listing=listing,
        price=price,
        annual_rent=annual_rent,
        lawyer_fee=lawyer_fee,
        caution_fee=caution_fee,
        has_c_of_o=has_c_of_o
    )

    new_prop = Property(title=prop.title,
                        city=prop.city,
                        area=prop.area,
                        bedrooms=prop.bedrooms,
                        listing=prop.listing,
                        price=prop.price,
                        annual_rent=prop.annual_rent,
                        lawyer_fee=prop.lawyer_fee,
                        caution_fee=prop.caution_fee,
                        has_c_of_o=prop.has_c_of_o,
                        user_id=cur_user.id)

    db.add(new_prop)
    db.flush()

    for med in media or []:
        media_file = verify_photo(med)
        new_media = PropertyMedia(
            filename=media_file.get("filename"),
            filepath=media_file.get("filepath"),
            media_type=media_file.get("media_type"),
            property_id=new_prop.id
        )

        db.add(new_media)

    db.commit()

    return {"msg": f"{prop.title} and its media files added successfully"}


# view all properties
@app.get("/properties")
def view_all_properties(page: int = 1, per_page: int = 3, db: Session = Depends(get_db)):
    offset = (page - 1) * per_page

    all_props = db.query(Property).filter_by(status=PropertyStatus.APPROVED).offset(offset).limit(per_page).all()
    props_count = db.query(Property).filter_by(status=PropertyStatus.APPROVED).count()

    results = []

    for prop in all_props:
        results.append({
            "id": prop.id,
            "title": prop.title,
            "city": prop.city,
            "area": prop.area,
            "bedrooms": prop.bedrooms,
            "listing": prop.listing,
            "status": prop.status,
            "price": prop.price,
            "annual_rent": prop.annual_rent,
            "lawyer_fee": prop.lawyer_fee,
            "caution_fee": prop.caution_fee,
            "has_c_of_o": prop.has_c_of_o
        })

    return {
        "page": page,
        "per_page": per_page,
        "total_pages": ceil(props_count / per_page),
        "results": results
    }


# view one property
@app.get("/properties/{prop_id}")
def view_one_property(prop_id: int, db: Session = Depends(get_db)):
    target = db.query(Property).filter_by(id=prop_id, status=PropertyStatus.APPROVED).first()

    if not target:
        raise HTTPException(404, "Not Found")

    return target


# update property
@app.patch("/properties/{prop_id}")
def update_property(prop_id: int, update_prop: UpdateProp, curr_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    target = db.query(Property).filter_by(id=prop_id, status=PropertyStatus.APPROVED).first()

    if not target:
        raise HTTPException(404, "Not Found")

    if target.user_id != curr_user:
        raise HTTPException(403, "You can only edit your properties")

    update_dict = update_prop.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(target, key, value)

    db.commit()
    return {"msg": "update successful"}


# Property sold out or rented out
@app.patch("/properties/sold/rented/{prop_id}")
def prop_unavail(prop_id: int, prop_sold: PropNotAvail, curr_user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    target = db.query(Property).filter_by(id=prop_id, status=PropertyStatus.APPROVED).first()

    if not target:
        raise HTTPException(404, "Not Found")

    if target.user_id != curr_user.id and curr_user.role != UserRole.ADMIN:
        raise HTTPException(403, "Only admin or owner can do this")

    prop_sold_dict = prop_sold.model_dump(exclude_unset=True)

    for key, value in prop_sold_dict.items():
        setattr(target, key, value)

    db.commit()
    return {"msg": "Sold/Rented Successful"}


# create sell item
@app.post("/item")
def create_item():
    pass


# create artisan
@app.post("/artisan")
def create_artisan():
    pass


# create sales
@app.post("/sales")
def create_sales():
    pass


Base.metadata.create_all(bind=engine)


