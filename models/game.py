from sqlalchemy import Sequence, Column, UniqueConstraint, Integer, String

from models.database import Base

game_seq = Sequence('game_id_seq')


class Game(Base):
    __tablename__ = 'game'
    # __abstract__ = True

    id = Column(Integer, default=game_seq, primary_key=True, unique=True, index=True)
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

    def __repr__(self):
        return f"<Game (id={self.id}, guest={self.customer}, " \
               f"guest_image={self.customer_image}, main={self.main}, " \
               f"main_image={self.main_image}, score={self.score}, " \
               f"people={self.people}, place={self.place}, " \
               f"event_date={self.event_date}, season={self.season})>"

    def __init__(self, id, customer, customer_image, main, main_image, score, people, place,
                 event_date, season, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.id = id
        self.customer = customer
        self.customer_image = customer_image
        self.main = main
        self.main_image = main_image
        self.score = score
        self.people = people
        self.place = place
        self.event_date = event_date
        self.season = season
