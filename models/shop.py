from models.database import Base
from sqlalchemy import Sequence, Column, UniqueConstraint, Integer, String



shop_seq = Sequence('stream_id_seq')


class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, shop_seq, primary_key=True, server_default=shop_seq.next_value())
    link = Column(String(255))
    image = Column(String(255))
    product = Column(String(255))
    price = Column(String(12))
    __table_args__ = (UniqueConstraint('product', name='product_unique'),)

    def __repr__(self):
        return f"<Stream (id={self.id}, link={self.link}, " \
               f"image={self.image}, product={self.product}, " \
               f"price={self.price})>"

    def __init__(self, id, link, image, product, price, **kwargs):
        super(Shop, self).__init__(**kwargs)
        self.id = id
        self.link = link
        self.image = image
        self.product = product
        self.price = price
