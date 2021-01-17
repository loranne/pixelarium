# script to seed pixelarium database

import os
# import json
# from random import choice, randint
# from datetime import datetime

import crud
from model import connect_to_db, db, Image, ImageTag, Tag
import server
import json
import cloudinary.api
import os
import utilities

# always drop then create

def initialize_db():
    """starts up database from scratch"""
    os.system('dropdb pixelarium')
    os.system('createdb pixelarium')

    # connect to the database and set up models with db.create_all
    connect_to_db(server.app)
    db.create_all()

initialize_db()

######################### API CALLS ############################

def get_images_data():
    """Gets JSON of all images in my cloudinary account, and converts to python dict"""

    url = "https://API_KEY:SECRET_API_KEY@api.cloudinary.com/v1_1/pixelarium/resources/image"

    # response = requests.get(url, params=payload)
    images_dict = cloudinary.api.resources(tags=True,
                                        max_results=500,
                                        metadata=True)

    # do not need to dictionary-ify it because it already behaves like a python dict

    return images_dict

################### CREATE RECORDS ###########################

def create_images(dict):
    """Create image records from cloudinary Admin API"""

    # iterate through lists in resources
    for image in dict["resources"]:
        # pulls secure_url and public_id from API call
        new_img = Image(link=image["secure_url"], title=image["public_id"])
        # add each time through loop
        db.session.add(new_img)
        db.session.commit()

def create_tags_and_relationships(dict):
    """Create tag records and relationships to images"""

    # iterates through all resources
    for image in dict["resources"]:

        # gets record object for image from db
        # needed for image_tags
        current_img = Image.query.filter_by(title=image["public_id"]).first()
        # added to accommodate re-running on server.py
        if current_img is not None:
            # iterates through tags by image
            for tag in image["tags"]:
                # query to find out if tag is already in db
                current_tag = Tag.query.filter_by(text=tag).first()
                # if it's not, create & commit it!
                if current_tag is None:
                    new_tag = Tag(text=tag)
                    db.session.add(new_tag)
                    # have to commit here instead of at end because we need these
                    # records for the rest of the function
                    db.session.commit()

                # now we have to set up the relationship
                # query gets the record for the just added tag
                added_tag = Tag.query.filter_by(text=tag).first()

                # uses tag id from just added tag, and img id from current image
                # which is determined by outer loop
                new_img_tag = ImageTag(img_id=current_img.img_id, tag_id=added_tag.tag_id)
                # add & commit to db
                db.session.add(new_img_tag)
                db.session.commit() 

################### CALLING FUNCTIONS #########################
# call functions to create data
# create_image()
# create_tag()
# create_image_tag_relationship()