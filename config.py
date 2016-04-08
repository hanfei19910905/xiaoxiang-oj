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
    DATABASE={
                'name': 'xiaoxiang_oj',
                'engine': 'peewee.MySQLDatabase',
                'user' : 'root',
                'password' : '123456',
                'host' : '127.0.0.1'
            }

config = {
    'default' : DevConfig
}
