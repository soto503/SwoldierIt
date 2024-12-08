import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'  # Change this to a strong secret key
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'swoldier.cv0qs42yqp2y.us-east-2.rds.amazonaws.com'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'cyberdudes'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'Cybi123!'
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'swoldier'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or '3306'

    @staticmethod
    def init_app(app):
        pass  # Can add app-specific initialization here if needed
