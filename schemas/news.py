from pydantic import BaseModel

class NewsBase(BaseModel):

    id: int
    link: str
    image: str
    date: str
    tag: str

class News(NewsBase):
    class Config:
        orm_mode = True