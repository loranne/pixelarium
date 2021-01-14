# script to seed pixelarium database

import os
# import json
# from random import choice, randint
# from datetime import datetime

import crud
from model import connect_to_db, db, Image, ImageTag, Tag
import server


# always drop then create
os.system('dropdb pixelarium')
os.system('createdb pixelarium')

# connect to the database and set up models with db.create_all
connect_to_db(server.app)
db.create_all()

######################### API CALLS ############################

def get_images_data():
    """Gets JSON of all images in my cloudinary account"""

    url = "https://API_KEY:SECRET_API_KEY@api.cloudinary.com/v1_1/pixelarium/resources/image"

    # response = requests.get(url, params=payload)
    response = cloudinary.api.resources()

    return response

    # data = response.json()

    # return render_template('search-results.html',
                        #    pformat=pformat,
                        #    data=data,
                        #    results=events)

################### CREATE RECORDS ###########################

# def create_image():
#     """Create image record"""

#     img = Image(link=, title=, desc=None, upload_date=, created_date=)
#     db.session.add(img)
#     db.session.commit()

# def create_tag():
#     """Create tag record"""

#     tag = Tag(text=)
#     db.session.add(tag)
#     db.session.commit()


# def create_image_tag_relationship():
#     """Create record in image_tags - relationship between tag and image"""

#     img_tag = ImageTag(img_id=, tag_id=)
#     db.session.add(img_tag)
#     db.session.commit()

################### CALLING FUNCTIONS #########################
# call functions to create data
# create_image()
# create_tag()
# create_image_tag_relationship()