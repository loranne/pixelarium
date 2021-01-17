# server for image repo experiment - pixelarium

from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Image, Tag, ImageTag
import os
import crud
import seed
import secrets
from datetime import datetime
from jinja2 import StrictUndefined

# has my colorizer function (print_color)
import utilities
import cloudinary.api

app = Flask(__name__)
app.secret_key = "FLASK_SECRET_KEY"
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

@app.route("/", methods=["GET", "POST"])
def homepage():
    """View homepage"""
    utilities.print_color("Homepage is go!")

    return render_template("homepage.html")


@app.route("/upload", methods=["GET", "POST"])
def upload_page():
    """User can upload images"""

    if request.method == "POST":
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

        # return render_template("upload.html")

    return render_template("upload.html")


@app.route("/results", methods=["POST"])
def search_results():
    """Search results"""

    # images_dict = seed.get_images_data()

    # seed.create_tags_and_relationships(images_dict)

    search_terms = request.form.get("search")

    search_results = crud.search_images(search_terms)

    return render_template("results.html", search_results=search_results, search_terms=search_terms)


@app.route("/images_test")
def show_all_image_data():
    """"Shows all images from my account"""
    print(f"\n {API_KEY} \n?")

    # url = f"https://{API_KEY}:{SECRET_API_KEY}@api.cloudinary.com/v1_1/pixelarium/resources/image"

    # response = requests.get(url, params=payload)
    response = cloudinary.api.resources(tags = True,
                                        max_results = 500)

    return response


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
if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')