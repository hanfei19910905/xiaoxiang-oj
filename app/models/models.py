from .. import db
from peewee import *
from flask_login import UserMixin
#from hashlib import md5
#from werkzeug.security import check_password_hash


class User(UserMixin, db.Model):
    email = CharField(unique=True)
    name = CharField()
    password = CharField()
    salt = CharField()
    #admin = BooleanField()

    def verify_password(self, password):
        return self.password == password

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name + ", " + self.email


class TrainCamp(db.Model):
    name = CharField(unique=True)
    begin_time = DateTimeField()
    end_time = DateTimeField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class CampUserRelationShip(db.Model):
    user_id = ForeignKeyField(User)
    camp_id = ForeignKeyField(TrainCamp)

    class Meta:
        indexes = (
            (('user_id', 'camp_id'), True),
        )


class HomeWork(db.Model):
    camp = ForeignKeyField(TrainCamp)
    name = CharField()
    #prob_count = IntegerField()
    #submit_count = IntegerField()
    begin_time = DateTimeField()
    end_time = DateTimeField()

    def __str__(self):
        return self.name


class Data(db.Model):
    name = CharField(unique=True, index=True)
    train = BlobField()
    test1= BlobField()
    test2 = BlobField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class JudgeNorm(db.Model):
    code = TextField()
    name = CharField()
    value = DecimalField()

    def  __str__(self):
        return self.name

class Problem(db.Model):
    name = CharField(null=False)
    author = CharField()
    data_id = ForeignKeyField(Data)
    description = TextField()
    judge_id = ForeignKeyField(JudgeNorm)


class HomeWorkProbRelationShip(db.Model):
    work_id = ForeignKeyField(HomeWork)
    prob_id = ForeignKeyField(Problem)
    show_id = CharField(10)

    class Meta:
        indexes = (
            (('work_id', 'prob_id'), True),
        )


class Submission(db.Model):
    user = ForeignKeyField(User, index=True)
    form = ForeignKeyField(HomeWorkProbRelationShip)
    score = IntegerField()
    source = TextField()
    status = CharField(10)
    time = DateTimeField()
