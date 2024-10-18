from pydantic import BaseModel, ConfigDict


class ClothingResponse(BaseModel):
    name: str


class SizeResponse(BaseModel):
    size: str
    quantity: int

    model_config = ConfigDict(from_attributes=True)
