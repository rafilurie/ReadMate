from app import db

from flask_user import UserMixin
from sqlalchemy import Column, ForeignKey, Integer, String


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')

    email = db.Column(db.String(120), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    is_enabled = db.Column(db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')

    def is_active(self):
        return self.is_enabled
    
    def __repr__(self):
        return '<User %r>' % (self.username)
