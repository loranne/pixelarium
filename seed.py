# script to seed pixelarium database

import os
# import json
# from random import choice, randint
# from datetime import datetime

import crud
from model import connect_to_db, db, Image, ImageTag, Tag
import server
import json
import requests


# always drop then create
os.system('dropdb pixelarium')
os.system('createdb pixelarium')

# connect to the database and set up models with db.create_all
connect_to_db(server.app)
db.create_all()

######################### API CALLS ############################

def get_images_data():
    """Gets JSON of all images in my cloudinary account, and converts to python dict"""

    url = "https://API_KEY:SECRET_API_KEY@api.cloudinary.com/v1_1/pixelarium/resources/image"

    # response = requests.get(url, params=payload)
    response = cloudinary.api.resources(tags = True,
                                        max_results = 500,
                                        metadata = True)

    images_dict = json.loads(response)

    return images_dict

################### CREATE RECORDS ###########################

def create_image(images_dict):
    """Create image record"""

    for image in images_dict:
        new_img = Image(link=secure_url, title=public_id)
        db.session.add(new_img)

    db.session.commit()


def create_tag(images_dict):
    """Create tag record"""

    #TODO: figure out how I'm grabbing the img_id...
    for image in images_dict:

        this_img = Image.query.filter_by(title=public_id)
        
        for tag in images_dict["tags"]:
            print(tag)
            new_tag = Tag(text=tag)
            print(new_tag)
            db.session.add(new_tag)
            db.session.commit()


            this_tag = Tag.query.filter_by(text=new_tag.text)
            print(this_tag)

            new_img_tag = ImageTag(img_id=this_img.img_id, tag_id=this_tag.tag_id)
            print(new_img_tag)
            db.session.add(new_img_tag)
            db.session.commit() 
        
def create_image_tag_relationship():
    """Create record in image_tags - relationship between tag and image"""

    img_tag = ImageTag(img_id=, tag_id=)
    db.session.add(img_tag)
    db.session.commit()

def 

################### CALLING FUNCTIONS #########################
# call functions to create data
# create_image()
# create_tag()
# create_image_tag_relationship()