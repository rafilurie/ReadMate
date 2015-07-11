import os, time
from app import app, db
from flask import render_template, request, jsonify, abort, Response, url_for, redirect
from werkzeug import secure_filename

@app.route("/")
def index():
    return redirect(url_for("welcome"))

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            # store file in DB - DON'T SAVE
            filename = secure_filename(file.filename) # change this to photo.id
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # save file in DB after it is in file system
            return redirect(url_for("detail"))
    return render_template("upload_file.html")

@app.route("/welcome")
def welcome():
    return render_template("index.html")

# private, associated with the user
@app.route("/photos")
def photos():
	return render_template("photos.html")

# private, associated with the user
# as of 11:11am, going to associate chat with the detail view
@app.route("/detail")
def detail():
	return render_template("detail.html")
