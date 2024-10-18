import re

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

letters = re.compile(r'^[а-яА-Яa-zA-Z\-]+$')


class CreateOrder(BaseModel):
    name: str = Field(min_length=3, max_length=20, description='Name clothing should '
                                                               'contains only letters')
    size: str = Field(description='Size clothes (xxs, xs, s, m, l, xl, xxl, xxxl')

    @field_validator('name')
    def validate_name_clothing(cls, value):
        if not letters.match(value):
            raise HTTPException(
                status_code=422,
                detail='Name clothing should contains only letters'
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
            status_code=400,
            detail=f'Size should be in: {sizes}'
        )
