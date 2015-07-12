import re

from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from validate_email import validate_email
from .models import User

def enforce_password_requirements(password):
    digits = re.search('[0-9]', password)
    special_characters = re.search("[^A-Za-z0-9]", password)
    uppercase = re.search("[A-Z]", password)
    lowercase = re.search("[a-z]", password)
    
    if len(password) < 7:
        return False
    if not digits:
        return all([uppercase, lowercase, special_characters])
    if not special_characters:
        return all([uppercase, lowercase, digits])
    if not lowercase:
        return all([uppercase, special_characters, digits])
    if not uppercase:
        return all([lowercase, digits, special_characters])

    return True