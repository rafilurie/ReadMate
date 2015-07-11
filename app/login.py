import re

from validate_email import validate_email


def enforce_password_requirements(password):
    digits = re.search('[0-9]', password)
    special_characters = re.search("[^A-Za-z0-9]", password)
    uppercase = re.search("[A-Z]", password)
    lowercase = re.search("[a-z]", password)
    
    if not digits:
        return all([uppercase, lowercase, special_characters]):
    if not special_characters:
    	return all([uppercase, lowercase, digits]):
    if not lowercase:
    	return all([uppercase, special_characters, digits]):
    if not uppercase:
    	return all([lowercase, digits, special_characters]):

    return True

def create_login(email, password):
    ''' Validate the email and enforce things about the password.
        Then, when validated, save the user to the database.
    '''    
    valid_email = validate_email(email)
    valid_password = enforce_password_requirements(password)

    if not valid_email:
    	raise ValueError("Email {} is not valid!".format(email))

    if not valid_password:
    	raise ValueError("Password {} is not valid!".format(password))

