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

class LoginForm(Form):
    username = StringField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            username=self.username.data).first()
        
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        valid_email = validate_email(self.username)
        valid_password = enforce_password_requirements(self.password)

        if not valid_email:
            self.username.errors.append('Email {} is not valid!'.format(email))
            return False

        pw_error_message = """Password is not valid. Password must have at least 7
                              characters and contain 3 of the following: uppercase
                              letters, lowercase letters, special characters, digits"""

        if not valid_password:
            self.password.errors.append(pw_error_message)
            return False

        self.user = user
        return True
