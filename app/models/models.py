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

class Contest(db.Model):
    id = PrimaryKeyField()
    contest_name = CharField()
    begin_time = DateTimeField()
    end_time = DateTimeField()

class Judge_way(db.Model):
    id = PrimaryKeyField()
    judge_code = CharField()

class Problem(db.Model):
    id = PrimaryKeyField()
    contest_id = ForeignKeyField(Contest)
    name = CharField()
    show_id = CharField()
    description = TextField()
    time_limit = IntegerField()
    mem_limit = IntegerField()
    input = TextField()
    output = TextField()
    judge_id = ForeignKeyField(Judge_way)

class Submission(db.Model):
    id = PrimaryKeyField()
    user_id = ForeignKeyField(User)
    prob_id = ForeignKeyField(Problem)
    status = IntegerField()
    source = CharField()
    time = DateTimeField()
