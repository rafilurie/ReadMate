from app import db

from flask_user import UserMixin
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    jeopardy_password = db.Column(db.String(255), nullable=False, server_default='')

    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')

    email = db.Column(db.String(120), nullable=False, unique=True)
    created = db.Column(db.DateTime())
    deleted = db.Column(db.DateTime())

    # What is this?
    is_enabled = db.Column(db.Boolean(), nullable=False, server_default='0')

    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')

    photos = db.relationship('Photo', backref='user', lazy='dynamic')
    perpetrators = db.relationship('Perpetrator', backref='user', lazy='dynamic')

    def is_active(self):
        return self.is_enabled

    def __repr__(self):
        return '<User %r>' % (self.username)


class Perpetrator(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime())
    deleted = db.Column(db.DateTime())

    name = db.Column(db.String(40), nullable=False)
    display_name = db.Column(db.String(40))

    # the user associated with this perpetrator
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Perpetrator %r, %r>' % (self.name, self.user_id)

    def __init__(self, name, user__id):
        self.name = name
        self.user_id = user_id


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    comments = db.relationship('Comment', secondary=words, backref=db.backref('sets', lazy='joined'))

    created = db.Column(db.DateTime())
    deleted = db.Column(db.DateTime())

    filename = db.Column(db.String(1000))
    name = db.Column(db.String(40))

    # the user associated with this perpetrator
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Photo %r, %r>' % (self.name, self.user_id)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100000))

    created = db.Column(db.DateTime())
    deleted = db.Column(db.DateTime())

    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))

    def __repr__(self):
        return '<Comment %r, %r>' % (self.content, self.photo_id)

    def __init__(self, name, photo_id):
        self.content = content
        slf.photo_id = photo_id
