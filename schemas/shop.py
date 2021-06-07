from pydantic import BaseModel

class ShopBase(BaseModel):

    id: int
    link: str
    image: str
    product: str
    price: str

class Shop(ShopBase):
    class Config:
        orm_mode = True