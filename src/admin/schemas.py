import re
from datetime import date

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict

letters = re.compile(r'^[а-яА-Яa-zA-Z\-]+$')


class CreateClothing(BaseModel):
    name: str = Field(min_length=3, max_length=20, description='Name clothing should '
                                                               'contain only letters')
    size: str = Field(description='Size clothes (xxs, xs, s, m, l, xl, xxl, xxxl')
    quantity: int = Field(gt=0, description='Quantity clothes more > 0')

    @field_validator('name')
    def validate_name_clothing(cls, value):
        if not letters.match(value):
            raise HTTPException(
                status_code=422,
                detail='Name clothing should contain only letters'
            )
        value_correct = value.capitalize()
        return value_correct

    @field_validator('size')
    def validate_size(cls, value):
        sizes = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']
        value_correct = value.upper()
        if value_correct in sizes:
            return value_correct
        raise HTTPException(
            status_code=422,
            detail=f'Size should be in: {sizes}'
        )

    model_config = ConfigDict(from_attributes=True)


class DeleteClothing(BaseModel):
    name: str = Field(min_length=3, max_length=20, description='Name clothing should '
                                                               'contain only letters, '
                                                               'first character capital')

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    name: str
    surname: str
    birthdate: date
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class OrdersUser(BaseModel):
    name_user: str
    birthdate: date
    email_user: EmailStr
    name_clothing: str
    size: str

    model_config = ConfigDict(from_attributes=True)
