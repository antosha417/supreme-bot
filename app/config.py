"""Basic functions and constans."""
from flask import session

APP_ID = u'5912386'
APP_SECRET_KEY = u'1htL3k7hevWf7tTFQ2zJ'
REDIRECT_URL = 'https://207.154.231.72/callback'
BASE_URL = 'https://207.154.231.72/'

KNOWN_COUNTRIES = ['RU']


def user_loggined():
    """Check if user is loggined."""
    if session.get('logged_in') is not None:
        if session['logged_in'] and session.get('user_id') is not None:
            return True
    return False


def check_int(str_, len_):
    """Check if str_ is int with given len_."""
    return str_ is not None and len(str_) == len_ and is_int(str_)


def is_int(str_):
    """Check if srt_ is int."""
    try:
        int(str_)
        return True
    except ValueError:
        return False
