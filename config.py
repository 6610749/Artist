import os 

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "my-secret-key"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://mohammed:mohammed123@localhost/Artist' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'cosmo'

    ADMIN_EMAIL = "info@lilagenda.nl"
    ADMIN_PASSWORD = "alertjenl"
    ADMIN_VERIFICATION = True
    RESULT_PER_PAGE = 4
