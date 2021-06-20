from sqlalchemy import Sequence, Column, UniqueConstraint, Integer, String

from models.database import Base

shop_seq = Sequence('stream_id_seq')


class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, shop_seq, primary_key=True, server_default=shop_seq.next_value())
    link = Column(String(255))
    image = Column(String(255))
    date = Column(String(12))
    tag = Column(String(25))
    description = Column(String(100))
    __table_args__ = (UniqueConstraint('description', name='desc_unique'),)

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
