from sqlalchemy import Sequence

from models.database import db

shop_seq = Sequence('stream_id_seq')


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, shop_seq, primary_key=True, server_default=shop_seq.next_value())
    link = db.Column(db.String(255))
    image = db.Column(db.String(255))
    date = db.Column(db.String(12))
    tag = db.Column(db.String(25))
    description = db.Column(db.String(100))
    __table_args__ = (db.UniqueConstraint('description', name='desc_unique'),)

    def __repr__(self):
        return f"<Stream (id={self.id}, link={self.link}, " \
               f"image={self.image}, date={self.date}, " \
               f"tag={self.tag}, description={self.description})>"

    def __init__(self, id, link, image, date, tag, description, **kwargs):
        super(News, self).__init__(**kwargs)
        self.id = id
        self.link = link
        self.image = image
        self.date = date
        self.tag = tag
        self.description = description
