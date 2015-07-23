from app import db
from flask_user import UserMixin
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime
from flask import url_for


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    jeopardy_password = db.Column(db.String(255), nullable=False, server_default='password')

    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')

    email = db.Column(db.String(120), nullable=False, unique=True)
    created = db.Column(db.DateTime())
    deleted = db.Column(db.DateTime())

    is_enabled = db.Column(db.Boolean(), nullable=False, server_default='0')

    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')

    photos = db.relationship('Photo', backref='user', lazy='dynamic')
    perpetrators = db.relationship('Perpetrator', backref='user', lazy='dynamic')
    articles = db.relationship('Article', backref='user', lazy='dynamic')

    def is_active(self):
        return self.is_enabled

    def __init__(self, username, password):
        self.email = username
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)

    @classmethod
    def get(cls,id):
        return cls.user_database.get(id)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime())

    # the user associated with this article
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(40), nullable=False)
    url = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return '<Article %r, %r>' % (self.title, self.user_id)

    def get_article_url(self):
        return self.url

    def __init__(self, title, user_id, url):
        self.title = title
        self.user_id = user_id
        self.url = url
        self.created = datetime.now()

class Perpetrator(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime())
    deleted = db.Column(db.DateTime())

    name = db.Column(db.String(40), nullable=False)
    display_name = db.Column(db.String(40))
    photos = db.relationship('Photo', backref=db.backref('perpetrators', lazy='joined'),
                               lazy='dynamic')

    # the user associated with this perpetrator
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Perpetrator %r, %r>' % (self.name, self.user_id)

    def get_photo_url(self):
        return "/reported/{0}/photos".format(self.id)

    def __init__(self, name, display_name, user_id):
        self.name = name
        self.user_id = user_id
        self.display_name = display_name
        self.created = datetime.now()


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    comments = db.relationship('Comment', backref=db.backref('photos', lazy='joined'),
                               lazy='dynamic')

    created = db.Column(db.DateTime())
    when = db.Column(db.DateTime())
    deleted = db.Column(db.DateTime())

    extension = db.Column(db.String(1000))

    # the user associated with this photo
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    perpetrator_id = db.Column(db.Integer, db.ForeignKey('perpetrator.id'))

    def list_comments(self):
        return self.comments.all()

    def get_url(self):
        url = "/images/{0}.{1}".format(self.id, self.extension)
        return url

    def get_help_url(self):
        url = "/detail/{0}".format(self.id)
        return url

    def __repr__(self):
        return '<Photo %r, %r>' % (self.extension, self.user_id)

    def __init__(self, extension, user_id, when=datetime.now()):
        self.extension = extension
        self.user_id = user_id
        self.created = datetime.now()
        self.when = when


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100000))

    created = db.Column(db.DateTime())
    deleted = db.Column(db.DateTime())

    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))

    def __repr__(self):
        return '<Comment %r, %r>' % (self.content, self.photo_id)

    def __init__(self, content, photo_id):
        self.content = content
        self.photo_id = photo_id
        self.created = datetime.now()
