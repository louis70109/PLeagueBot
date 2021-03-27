from sqlalchemy import Sequence

from models.database import db

stream_seq = Sequence('stream_id_seq')


class Stream(db.Model):
    __tablename__ = 'stream'
    id = db.Column(db.Integer, stream_seq, primary_key=True, server_default=stream_seq.next_value())
    link = db.Column(db.String(255))
    image = db.Column(db.String(255))
    title = db.Column(db.String(100))
    is_live = db.Column(db.Boolean(), default=True)
    __table_args__ = (db.UniqueConstraint('link', 'image', 'title', name='stream_unique'),)

    def __repr__(self):
        return f"<Stream (id={self.id}, link={self.link}, " \
               f"image={self.image}, tile={self.tile}, " \
               f"is_live={self.is_live})>"

    def __init__(self, id, link, image, tile, is_live, **kwargs):
        super(Stream, self).__init__(**kwargs)
        self.id = id
        self.link = link
        self.image = image
        self.tile = tile
        self.is_live = is_live
