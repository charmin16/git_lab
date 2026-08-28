from pydantic import BaseModel, Field, model_validator, field_validator
from enums import ListingType, PropertyStatus
from fastapi import HTTPException


class CreateProperty(BaseModel):
    title: str
    city: str
    area: str
    bedrooms: int
    listing: ListingType
    status: PropertyStatus
    price: float
    annual_rent: float
    lawyer_fee: float
    caution_fee: float
    has_c_of_o: bool
    user_id: int

    @model_validator(mode="after")
    def validate_listing(self):
        if self.listing == ListingType.RENT:
            if self.annual_rent is None:
                raise ValueError("Annual Rent is Required")

            if self.caution_fee is None:
                raise ValueError("Caution Fee is Required")

            if self.price is not None:
                raise ValueError("Price is not required. Its on for properties on sale")

            if self.has_c_of_o is not None:
                raise ValueError("C_of_O is not required for rented property")

        elif self.listing == ListingType.SALE:
            if self.annual_rent is not None:
                raise ValueError("Rent is not required")

            if self.price is None:
                raise ValueError("Price is required for Property on sale")

        return self

