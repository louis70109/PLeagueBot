from models.database import Base
from sqlalchemy import Sequence, Column, Integer, String

player_rank_seq = Sequence('player_rank_id_seq')


class PlayerRank(Base):
    __tablename__ = 'player_rank'
    id = Column(Integer, player_rank_seq, primary_key=True,
                   server_default=player_rank_seq.next_value())
    player = Column(String(10))
    team = Column(String(10))
    average = Column(String(10))
    rank_name = Column(String(10))

    def __repr__(self):
        return f"<PlayerRank (id={self.id}, " \
               f"player={self.player}, team={self.team}, average={self.average}, " \
               f"rank_name={self.rank_name})>"

    def __init__(self, id, player, team, average, rank_name, **kwargs):
        super(PlayerRank, self).__init__(**kwargs)
        self.id = id
        self.player = player
        self.team = team
        self.average = average
        self.rank_name = rank_name
