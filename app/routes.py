import os, time
import cgi
from app import app, db
from flask.ext.login import login_user, logout_user
from flask import session, render_template, request, jsonify, abort, Response, url_for, redirect, flash, send_from_directory
from flask_user import login_required
from werkzeug import secure_filename
from models import *

from flask.ext.login import LoginManager
from login import enforce_password_requirements
from validate_email import validate_email


@app.route("/")
def index():
    return redirect(url_for("welcome"))

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    try:
        logged_in_user = session["user_id"]
    except KeyError:
        return redirect(url_for("index"))

    if request.method == "POST":
        file = request.files["file"]
        if file:
            try:
                # add to database
                extension = file.filename.rsplit(".", 1)[1]
                db_file = Photo(extension, logged_in_user, datetime.strptime(request.form["date"], "%Y-%m-%d"))
                db.session.add(db_file)
                db.session.flush()
                db_comment = Comment(request.form["content"], db_file.id)
                if not Perpetrator.query.filter(Perpetrator.name == request.form["name"] and Perpetrator.user_id == logged_in_user).all():
                    db_perp = Perpetrator(request.form["name"], "", logged_in_user)
                    db.session.add(db_perp)
                    db.session.flush()
                    db_file.perpetrator_id = db_perp.id
                else:
                    existing_perp = Perpetrator.query.filter(Perpetrator.name == request.form["name"] and Perpetrator.user_id == logged_in_user).one()
                    db_file.perpetrator_id = existing_perp.id
                db.session.add(db_file)
                db.session.add(db_comment)
                db.session.commit()

                # save to file system
                filename = "{0}.{1}".format(db_file.id, extension)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                flash("Your photo was uploaded")
                return redirect(url_for("perps"))
            except:
                error = "Error saving file, please try again."
        else:
            error = "No photo was supplied."
        return render_template("upload_file.html", error=error)
    return render_template("upload_file.html")

@app.route("/welcome/login", methods=["GET", "POST"])
def login():
    try:
        password = request.form["password"]
        username = request.form["username"]
    except:
        return render_template("index.html", form=request.form, error="No username or password provided.")

    if enforce_password_requirements(password) and validate_email(username):
        db_user = User.query.filter(User.username == username and User.password == password).all()
        if not db_user:
            return render_template("index.html", form=request.form, error="No user associated with that username and password.")
        login_user(db_user)
        db.session.add(db_user)
        db.session.commit()
        session["user_id"] = db_user.id
        return redirect(url_for("empty"))
    return render_template("index.html", form=request.form)

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    try:
        password = request.form["password"]
        username = request.form["username"]
    except:
        return render_template("index.html", form=request.form, error="No username or password provided.")

    if enforce_password_requirements(password) and validate_email(username):
        in_db = User.query.filter(User.username == username).all()
        if in_db:
            return render_template("index.html", form=request.form, error="User with that username already exists.")
        db_user = User(request.form["username"], request.form["password"])
        login_user(db_user)
        db.session.add(db_user)
        db.session.commit()
        session["user_id"] = db_user.id
        return redirect(url_for("empty"))
    return render_template("index.html", form=request.form)

@app.route("/empty")
def empty():
    try:
        logged_in_user = session["user_id"]
    except KeyError:
        return redirect(url_for("index"))

    return render_template("empty.html")

@app.route("/reported/<id>/photos")
def photos(id):
    try:
        logged_in_user = session["user_id"]
    except KeyError:
        return redirect(url_for("index"))
    
    perp = Perpetrator.query.get(id)
    session["photo_ids"] = [photo.id for photo in perp.photos]
    return render_template("photos.html", photos=perp.photos, perpname=perp.name)

@app.route("/counselor")
def counselor():
    try:
        logged_in_user = session["user_id"]
    except KeyError:
        return redirect(url_for("index"))

    return render_template("counselor.html")

@app.route("/detail/<id>")
def detail(id):
    try:
        logged_in_user = session["user_id"]
    except KeyError:
        return redirect(url_for("index"))

    if request.method == "POST":
        try:
            photo = Photo.query.filter_by(id).first()
            db_comment = Comment(request.form["content"], photo.id)
            db.session.add(db_comment)
            db.session.commit()
        except:
            error = "Error saving file, please try again."
        return render_template("detail.html", error=error)
    return render_template("detail.html")

@app.route("/logout")
def logout():
    logout_user()
    try:
        del session["user_id"]
    except KeyError:
        pass

    return redirect(url_for("welcome"))

@app.route("/images/<path>")
def send_img(path):
    try:
        logged_in_user = session["user_id"]
    except KeyError:
        return redirect(url_for("index"))

    return send_from_directory(app.config["UPLOAD_FOLDER"], path)

@app.route("/reported")
def perps():
    try:
        logged_in_user = session["user_id"]
    except KeyError:
        return redirect(url_for("index"))

    perps = User.query.get(logged_in_user).perpetrators.all()
    return render_template("perps.html", perps=perps)
