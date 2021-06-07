from pydantic import BaseModel

class StreamBase(BaseModel):

    id: int
    link: str
    image: str
    title: str
    is_live: bool

class Stream(StreamBase):
    class Config:
        orm_mode = True