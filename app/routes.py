from app import app, db
from flask import render_template, request, jsonify, abort, Response, url_for

@app.route("/welcome")
def index():
    return render_template("templates/index.html")

# private, associated with the user
@app.route("/photos")
def photos():
	return render_template("templates/photos.html")

# private, associated with the user
# as of 11:11am, going to associate chat with the detail view
@app.route("/detail")
def detail():
	return render_template("templates/detail.html")


