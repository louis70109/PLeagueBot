from models.database import Base
from sqlalchemy import Sequence, Column, Boolean, UniqueConstraint, Integer, String

stream_seq = Sequence('stream_id_seq')


class Stream(Base):
    __tablename__ = 'stream'
    id = Column(Integer, stream_seq, primary_key=True,
                   server_default=stream_seq.next_value())
    link = Column(String(255))
    image = Column(String(255))
    title = Column(String(100))
    is_live = Column(Boolean, default=True)
    __table_args__ = (UniqueConstraint('link', 'image', 'title', name='stream_unique'),)

    def __repr__(self):
        return f"<Stream (id={self.id}, link={self.link}, " \
               f"image={self.image}, tile={self.title}, " \
               f"is_live={self.is_live})>"

    def __init__(self, id, link, image, title, is_live, **kwargs):
        super(Stream, self).__init__(**kwargs)
        self.id = id
        self.link = link
        self.image = image
        self.title = title
        self.is_live = is_live
