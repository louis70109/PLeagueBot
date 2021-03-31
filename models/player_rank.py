from sqlalchemy import Sequence
from models.database import db

player_rank_seq = Sequence('player_rank_id_seq')


class PlayerRank(db.Model):
    __tablename__ = 'player_rank'
    id = db.Column(db.Integer, player_rank_seq, primary_key=True,
                   server_default=player_rank_seq.next_value())
    player = db.Column(db.String(10))
    team = db.Column(db.String(10))
    average = db.Column(db.String(10))
    rank_name = db.Column(db.String(10))

    def __repr__(self):
        return f"<PlayerRand (id={self.id}, " \
               f"player={self.player}, team={self.team}, average={self.average}, " \
               f"rank_name={self.rank_name})>"

    def __init__(self, id, player, team, average, rank_name, **kwargs):
        super(PlayerRank, self).__init__(**kwargs)
        self.id = id
        self.player = player
        self.team = team
        self.average = average
        self.rank_name = rank_name
