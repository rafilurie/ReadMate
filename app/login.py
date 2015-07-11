import re

from validate_email import validate_email

# May package this in a class later

def enforce_password_requirements(password):
    digits = re.search('[0-9]', password)
    special_characters = re.search("[^A-Za-z0-9]", password)
    uppercase = re.search("[A-Z]", password)
    lowercase = re.search("[a-z]", password)
    
    # This is ugly, sorry
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
	# validate the email address, enforce things about the password,
    valid_email = validate_email(email)
    valid_password = enforce_password_requirements(password)

    if not valid_email:
    	raise ValueError("Email {} is not valid!".format(email))

    if not valid_password:
    	raise ValueError("Password {} is not valid!".format(password))

    # store in the database and use flask user manager
    
# I think the usermanager probably does the rest of the work, but I'm not
# really sure.