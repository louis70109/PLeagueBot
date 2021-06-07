from pydantic import BaseModel

class GameBase(BaseModel):

    id: int
    customer: str
    customer_image: str
    main: str
    main_image: str
    score: str
    people: str
    place: str
    event_date: str
    season: str

class Game(GameBase):
    class Config:
        orm_mode = True