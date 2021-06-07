from pydantic import BaseModel

class PlayerRankBase(BaseModel):

    id: int
    player: str
    team: str
    average: str
    rank_name: str
    

class PlayerRank(PlayerRankBase):
    class Config:
        orm_mode = True