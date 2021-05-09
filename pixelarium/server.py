# server for image repo experiment - pixelarium

from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from .model import connect_to_db, db, Image, Tag, ImageTag
import os
from . import crud
import secrets
from datetime import datetime
from jinja2 import StrictUndefined
# has my colorizer function (log_color)
from . import utilities
import cloudinary.api
import sys

app = Flask(__name__)
app.secret_key = os.urandom(16)
app.debug = True
toolbar = DebugToolbarExtension(app)
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ.get("API_KEY")
SECRET_API_KEY = os.environ.get("SECRET_API_KEY")

cloudinary.config(
  cloud_name="pixelarium",
  api_key=API_KEY,
  api_secret=SECRET_API_KEY
)

############################ VIEW FUNCTIONS ########################

@app.route("/", methods=["GET", "POST"])
def homepage():
    """View homepage"""
    utilities.log_color("Homepage is go!")

    return render_template("homepage.html")


@app.route("/upload", methods=["GET", "POST"])
def upload_page():
    """User can upload images"""

    # gets data from upload widget log
    if request.method == "POST":
        # needed to create new records in db
        img_url = request.form.get("upload_result[secure_url]")
        img_title = request.form.get("upload_result[public_id]")
        img_tags = request.form.getlist("upload_result[tags][]")
        
        crud.create_image_from_upload(img_title, img_url)

        current_img = Image.query.filter_by(title=img_title).first()

        for tag in img_tags:
            current_tag = Tag.query.filter_by(text=tag).first()

            if current_tag is None:
                new_tag = Tag(text=tag)
                db.session.add(new_tag)
                db.session.commit()

            added_tag = Tag.query.filter_by(text=tag).first()

            new_img_tag = ImageTag(img_id=current_img.img_id, tag_id=added_tag.tag_id)
            db.session.add(new_img_tag)
            db.session.commit()

    return render_template("upload.html")


@app.route("/results", methods=["POST"])
def search_results():
    """Search results"""

    # takes in user input search string
    search_terms = request.form.get("search")

    # calls search function
    search_results = crud.search_images(search_terms)

    return render_template("results.html", search_results=search_results, 
                            search_terms=search_terms)


@app.route("/tag/<tag_id>")
def show_images_by_tag(tag_id):
    """Shows all images associated with a given tag"""

    tag = Tag.query.filter_by(tag_id=tag_id).one()

    images = tag.images

    return render_template("tag.html", images=images, tag=tag)


@app.route("/browse")
def show_all_images():
    """Shows all images and their tags"""

    images = Image.query.all()

    return render_template("browse.html", images=images)


########################## RUN IT ###########################
# uncomment below for running locally
if __name__ == '__main__':
    utilities.log_color("Runit happened!")
    import seed
    seed.populate_database(app)

    # comment out 116, uncomment 117 to run locally
    # app.run(debug=False, host='0.0.0.0', port=sys.argv[1])
    app.run(debug=False, host='0.0.0.0')