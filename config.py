import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '*********'  # Change this to a strong secret key
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or '*********'
    MYSQL_USER = os.environ.get('MYSQL_USER') or '******'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or '*******'
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or '*******'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or '*******'

    @staticmethod
    def init_app(app):
        pass  # Can add app-specific initialization here if needed
