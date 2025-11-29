import os
from dotenv import load_dotenv
load_dotenv()


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(BASE_DIR, "data", "app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
    ADMIN_PASS = os.environ.get('ADMIN_PASS', 'admin123')
