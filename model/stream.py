from api import db


class Stream(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(100))
    link = db.Column('link', db.String(255))
    image = db.Column('image', db.String(255))
    is_live = db.Column('is_live', db.Boolean(), default=False)

    def __init__(self, id, title, link, image, is_live):
        self.id = id
        self.title = title
        self.link = link
        self.image = image
        self.is_live = is_live
