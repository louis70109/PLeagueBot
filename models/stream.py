from sqlalchemy import Sequence

from models.database import db

game_seq = Sequence('game_id_seq')


class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, game_seq, primary_key=True, server_default=game_seq.next_value())
    customer = db.Column(db.String(50), nullable=False)
    customer_image = db.Column(db.String(200))
    main = db.Column(db.String(50), nullable=False)
    main_image = db.Column(db.String(200))
    score = db.Column(db.String(10))
    people = db.Column(db.String(15))
    place = db.Column(db.String(20))
    event_date = db.Column(db.String(30))
    __table_args__ = (db.UniqueConstraint('customer', 'main', 'place', 'event_date', name='game_unique'),)

    def __repr__(self):
        return f"<Game (id={self.id}, guest={self.customer}, " \
               f"guest_image={self.customer_image}, main={self.main}, " \
               f"main_image={self.main_image}, score={self.score}, " \
               f"people={self.people}, place={self.place}, " \
               f"event_date={self.event_date}>"

    def __init__(self, id, customer, customer_image, main, main_image, score, people, place, event_date, **kwargs):
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
