import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('REOJ_SECRET_KEY') or 'reoj is the best onlinejudge in the world!'
    REOJ_MAIL_SUBJECT_PREFIX = '[Reoj]'
    REOJ_MAIL_SENDER = 'Reoj Admin <reoj@reoj.com>'
    REOJ_ADMIN = os.environ.get('REOJ_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/xiaoxiang_oj'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

config = {
    'default' : DevConfig
}
