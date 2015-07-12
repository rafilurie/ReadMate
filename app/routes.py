import os, time
import cgi
from app import app, db
from flask.ext.login import login_user, logout_user
from flask import render_template, request, jsonify, abort, Response, url_for, redirect, flash
from flask_user import login_required
from werkzeug import secure_filename
from models import *

from flask.ext.login import LoginManager
from login import LoginForm


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
                if not Perpetrator.query.filter(Perpetrator.name == request.form["name"]
                    and Perpetrator.display_name == reuqest.form["display_name"]
                    and Perpetrator.user_id == 1).all():
                    db_perp = Perpetrator(request.form["name"], requset.form["display_name"], 1)
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
    from login import enforce_password_requirements

    form = LoginForm()
    print form
    print form.user
    print form.username
    print form.password
    print form.validate_on_submit()
    print enforce_password_requirements(form.password)
    if form.validate_on_submit():
        db.session["user_id"] = form.user.id
        redirect(url_for("empty"))
    return render_template("index.html", form=form)

@app.route("/welcome")
def welcome():
    return render_template("index.html")

@app.route("/empty")
def empty():
    return render_template("empty.html")

@app.route("/photos")
@login_required
def photos():
	return render_template("photos.html")

@app.route("/detail/<id>")
@login_required
def detail(id):
    photo = Photo.query.filter_by(id=id).first()
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for())

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("welcome"))
