import os, time
from app import app, db
from flask import render_template, request, jsonify, abort, Response, url_for, redirect
from flask.ext.login import login_user, logout_user
from flask_user import login_required
from werkzeug import secure_filename

from login import LoginForm


@app.route("/")
def index():
    return redirect(url_for("welcome"))

@app.route("/upload", methods=["GET", "POST"])
#@login_required
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            try:
                # store file in DB - DON'T SAVE
                filename = secure_filename(file.filename) # change this to photo.id
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # save file in DB after it is in file system
                flash("Your photo was uploaded")
                return redirect(url_for("detail"))
            except:
                error = "Error saving file, please try again."
        else:
            error = "No photo was supplied."
        return render_template("upload_file.html", error=error)
    return render_template("upload_file.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['user_id'] = form.user.id
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route("/welcome")
def welcome():
    return render_template("index.html")

@app.route("/photos")
#@login_required
def photos():
	return render_template("photos.html")

@app.route("/detail")
@login_required
def detail():
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for())
	return render_template("detail.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("welcome"))
