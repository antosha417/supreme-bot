"""Application config."""

import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
CSRF_ENABLED = True
SECRET_KEY = os.urandom(24)
UPLOAD_FOLDER = os.path.join(BASEDIR, 'files')
IMG_FOLDER = os.path.join(BASEDIR, 'imgs')
MAX_CONTENT_LENGTH = 200 * 1024 * 1024 + 32

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
