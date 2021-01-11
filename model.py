# Models for image repo for shopify internship application
# pixelarium

from flax_sqlalchemy import SQLAlchemy

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
# uncomment line below for running interactively
# import crud

db = SQLAlchemy()

class Image(db.Model):
    """An image"""

    __tablename__ = "images"

    img_id = db.Column(db.Integer, 
                        autoincrement=True,
                        primary_key=True)
    title = db.Column(db.String(50),
                        nullable=False)
    desc = db.Column(db.Text,
                        nullable=True)
    upload_date = db.Column(db.DateTime,
                        nullable=False)
    created_date = db.Column(db.DateTime)
    device = db.Column(db.Text,
                        nullable=True)

    # sets up many-to-many relationship with tags
    tags = db.relationship("Tag", secondary="image_tags")

    def __repr__(self):
        return f"<Image id={self.img_id} title={self.title} upload date={self.upload_date}>"


class Tag(db.Model):
    """A tag"""

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    text = db.Column(db.String(50),
                        nullable=False)

    images = db.relationship("Image", secondary="images")                    

    def __repr__(self):
        return f"<Tag id={self.tag_id} text={self.text}>"


class ImageTag(db.Model):
    """An association between Image and Tag"""

    __tablename__ = "image_tags"

    img_tag_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    img_id = db.Column(db.Integer,
                        db.ForeignKey("images.img_id"))
    tag_id = db.Column(db.Integer,
                        db.ForeignKey("tags.tag_id"))

    images = db.relationship("Image")
    tags = db.relationship("Tag")

    def __repr__(self):
        return f"<ImageTag id={self.img_tag_id} img_id={self.img_id} tag_id={self.tag_id}>"
        

def connect_to_db(flask_app, db_uri="postgresql:///ptremix", echo=True):
    """Connect to the DB"""
    
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

# for running model interactively and testing db
if __name__ == '__main__':
    from server import app
    # pulls in seed data
    import seed

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app, echo=False)