import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.googlemail.com' # os.environ.get('MAIL_SERVER')
    MAIL_PORT = 587 # int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = 1 # os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = 'barbearia.ope@gmail.com' # os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = 'impactaope'  # os.environ.get('MAIL_PASSWORD')
    ADMINS = ['barbearia.ope@gmail.com']