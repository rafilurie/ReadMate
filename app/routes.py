import os, time
from app import app, db
from flask import render_template, request, jsonify, abort, Response, url_for, redirect, flash, send_from_directory
from flask_user import login_required
from werkzeug import secure_filename
from models import *

@app.route("/")
def index():
    return redirect(url_for("welcome"))

@app.route("/upload", methods=["GET", "POST"])
# @login_required
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            try:
                # add to database
                extension = file.filename.rsplit(".", 1)[1]
                db_file = Photo(extension, 1) # TODO: change this to the current user's id
                db.session.add(db_file)
                db.session.flush()
                db_comment = Comment(request.form["content"], db_file.id)
                if not Perpetrator.query.filter(Perpetrator.name == request.form["name"] and Perpetrator.user_id == 1).all():
                    db_perp = Perpetrator(request.form["name"], "", 1) # TODO: change to the current user's id
                    db.session.add(db_perp)
                db.session.add(db_comment)
                db.session.commit()

                # save to file system
                filename = "{0}.{1}".format(db_file.id, extension)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                flash("Your photo was uploaded")
                return redirect(url_for("detail"))
            except:
                error = "Error saving file, please try again."
        else:
            error = "No photo was supplied."
        return render_template("upload_file.html", error=error)
    return render_template("upload_file.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session["user_id"] = form.user.id
        return redirect(url_for("index"))
    return render_template("login.html", form=form)

@app.route("/welcome")
def welcome():
    return render_template("index.html")

@app.route("/empty")
def empty():
    return render_template("empty.html")

@app.route("/photos")
#@login_required
def photos():
	return render_template("photos.html", photos=Photo.query.all())

@app.route("/detail")
#@login_required
def detail():
	return render_template("detail.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("welcome"))

@app.route('/images/<path>')
def send_img(path):
    return send_from_directory(app.config["UPLOAD_FOLDER"], path)
