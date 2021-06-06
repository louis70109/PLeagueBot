from sqlalchemy import Sequence, Column, UniqueConstraint, Integer, String

from models.database import Base

game_seq = Sequence('game_id_seq')


class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, default=game_seq, primary_key=True, server_default=game_seq.next_value())
    customer = Column(String(50))
    customer_image = Column(String(200))
    main = Column(String(50), nullable=False)
    main_image = Column(String(200))
    score = Column(String(10))
    people = Column(String(15))
    place = Column(String(20))
    event_date = Column(String(30))
    season = Column(String(20))
    __table_args__ = (
        UniqueConstraint('customer', 'main', 'place', 'event_date', name='game_unique'),)