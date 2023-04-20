import os
from string import ascii_letters, digits


ALLOWED_CHARACTERS = ascii_letters + digits
DEFAULT_SHORT_ID_LENGTH = 6
MAX_CUSTOM_ID_LENGTH = 16
MAX_ORIGINAL_LINK_LENGHT = 256
STATIC_DIR = os.path.abspath('./html')
TEMPLATE_DIR = os.path.join(STATIC_DIR, 'templates')


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
