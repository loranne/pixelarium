# Models for image repo for image repo experiment - pixelarium

from flask_sqlalchemy import SQLAlchemy

# uncomment line below for running interactively
# import crud
# comment out cloudinary and os stuff below before completing
import cloudinary.api
import os
import json

# uncomment lines below for heroku
API_KEY = os.environ.get("API_KEY")
SECRET_API_KEY = os.environ.get("SECRET_API_KEY")

cloudinary.config(
  cloud_name="pixelarium",
  api_key=API_KEY,
  api_secret=SECRET_API_KEY
)

db = SQLAlchemy()


class Image(db.Model):
    """An image"""

    __tablename__ = "images"

    img_id = db.Column(db.Integer, 
                        autoincrement=True,
                        primary_key=True)
    link = db.Column(db.String,
                        nullable=False)
    title = db.Column(db.String(50),
                        nullable=False)

    # sets up many-to-many relationship with tags
    tags = db.relationship("Tag", secondary="image_tags")

    def __repr__(self):
        return f"<Image id={self.img_id} title={self.title}"


class Tag(db.Model):
    """A tag"""

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    text = db.Column(db.String(50),
                        nullable=False)

    images = db.relationship("Image", secondary="image_tags")                    

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
        

# commment out 84 and 87, uncomment 83 for local
# def connect_to_db(flask_app, db_uri="postgresql:///pixelarium", echo=True):
def connect_to_db(flask_app, echo=True):
    """Connect to the DB"""

    db_uri = os.environ.get("HEROKU_POSTGRESQL_PUCE_URL")

    if db_uri.startswith("postgres://"):
        db_uri = db_uri.replace("postgres://", "postgresql://")
    
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

def sample_data():
    """Create example data for testing purposes"""

    img1 = Image(img_id=1, link="", title="Sample Image - Cats")
    img2 = Image(img_id=2, link="", title="Sample Image - Landscape")
    img3 = Image(img_id=3, link="", title="Sample Image - Travel")
    
    tag1 = Tag(tag_id=1, text="pets")
    tag2 = Tag(tag_id=2, text="cats")
    tag3 = Tag(tag_id=3, text="landscape")
    tag4 = Tag(tag_id=4, text="travel")
    tag5 = Tag(tag_id=5, text="italy")
    tag6 = Tag(tag_id=6, text="great outdoors")
    
    img_tag1 = ImageTag(img_id=1, tag_id=1)
    img_tag2 = ImageTag(img_id=1, tag_id=2)
    img_tag3 = ImageTag(img_id=2, tag_id=3)
    img_tag4 = ImageTag(img_id=2, tag_id=6)
    img_tag5 = ImageTag(img_id=2, tag_id=4)
    img_tag6 = ImageTag(img_id=3, tag_id=4)
    img_tag7 = ImageTag(img_id=3, tag_id=5)

    db.session.add(img1)
    db.session.add(img2) 
    db.session.add(img3) 
    db.session.add(tag1)
    db.session.add(tag2) 
    db.session.add(tag3) 
    db.session.add(tag4) 
    db.session.add(tag5) 
    db.session.add(tag6)
    db.session.add(img_tag1) 
    db.session.add(img_tag2) 
    db.session.add(img_tag3) 
    db.session.add(img_tag4) 
    db.session.add(img_tag5) 
    db.session.add(img_tag6) 
    db.session.add(img_tag7)

    db.session.commit()



########################## RUNNING FUNCTIONS ##########################

if __name__ == '__main__':
    from server import app
    # pulls in seed data
    # import seed

    # Call connect_to_db(app, echo=False) if program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    # uncomment to test interactively
    # os.system('dropdb pixelarium')
    # os.system('createdb pixelarium')

    connect_to_db(app, echo=False)
    db.create_all()
    