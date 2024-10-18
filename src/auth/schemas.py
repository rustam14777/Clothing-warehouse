import re
from datetime import date

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict

letters = re.compile(r'^[а-яА-Яa-zA-Z\-]+$')


class UserBase(BaseModel):
    name: str = Field(max_length=30, min_length=4, description='Name must be between 4 '
                                                               'and 30 characters and name should '
                                                               'contain'
                                                               'only letters')
    surname: str = Field(max_length=30, min_length=4, description='Surname must be between 4 '
                                                                  'and 30 characters and surname '
                                                                  'should contain only letters')
    email: EmailStr = Field(max_length=40, min_length=9, description='Email must be between 9 '
                                                                     'and 40 characters')
    birthdate: date = Field(description='Date of birthday format "2000-12-30"')

    @field_validator('name')
    def validator_name(cls, value):
        if not letters.match(value):
            raise HTTPException(
                status_code=422,
                detail='Name name should contain only letters'
            )
        return value.capitalize()

    @field_validator('surname')
    def validator_surname(cls, value):
        if not letters.match(value):
            raise HTTPException(
                status_code=422,
                detail='Surname name should contain only letters'
            )
        return value.capitalize()

    @field_validator('birthdate')
    def validator_birthdate(cls, value):
        if not date(1970, 1, 1) <= value < date(2018, 1, 1):
            raise HTTPException(
                status_code=422,
                detail='Must be in range 1970-2018'
            )
        return value
    model_config = ConfigDict(from_attributes=True)


class CreateUser(UserBase):
    password: str = Field(min_length=6, description='Length password must be more then 6')


class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    is_user: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None
