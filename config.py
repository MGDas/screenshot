import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(os.getcwd(), 'app', 'static', 'uploads')


class Config:
    LOCAL_PATH = 'postgresql://postgres:postgres@localhost/screenshot'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', LOCAL_PATH)
