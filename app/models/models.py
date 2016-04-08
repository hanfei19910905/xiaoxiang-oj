from .. import db
from peewee import *
from flask_login import UserMixin
from hashlib import md5
from werkzeug.security import check_password_hash

class User(UserMixin, db.Model):
    id = PrimaryKeyField()
    email = CharField(unique=True)
    name = CharField()
    password = CharField()
    salt = CharField()
    #admin = BooleanField()
    def verify_password(self, password):
        return self.password == password

