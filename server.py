# server for image repo experiment - pixelarium

from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Image, Tag, ImageTag
import os
# crud doesn't exist yet. not sure I'll need it
# import crud
import secrets
from datetime import datetime
from jinja2 import StrictUndefined

# has my colorizer function (print_color)
import utilities

app = Flask(__name__)
app.secret_key = "SECRETKEY"
app.debug = True
toolbar = DebugToolbarExtension(app)
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage"""
    print_color("Homepage is go!")

    return render_template("homepage.html")

@app.route("/upload", methods=["POST"])
def upload_img():
    """User can upload images"""

    return render_template("upload.html")