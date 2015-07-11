from app import app, db
from flask import render_template, request, jsonify, abort, Response, url_for

@app.route('/')
def index():
    return "Hello world!"
