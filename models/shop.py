from sqlalchemy import Sequence

from models.database import db

shop_seq = Sequence('stream_id_seq')


class Shop(db.Model):
    __tablename__ = 'shop'
    id = db.Column(db.Integer, shop_seq, primary_key=True, server_default=shop_seq.next_value())
    link = db.Column(db.String(255))
    image = db.Column(db.String(255))
    product = db.Column(db.String(255))
    price = db.Column(db.String(12))
    __table_args__ = (db.UniqueConstraint('product', name='product_unique'),)

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
