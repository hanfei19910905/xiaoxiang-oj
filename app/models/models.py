from .. import db
from sqlalchemy import *
from flask_login import UserMixin
#from hashlib import md5
#from werkzeug.security import check_password_hash

camp_user = db.Table('camp_user',
    db.Column('user_id', Integer, db.ForeignKey('user.id')),
    db.Column('traincamp_id', Integer, db.ForeignKey('traincamp.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'user' 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), unique=True)
    name = db.Column(db.String(200))
    password = db.Column(db.String(200))
    salt = db.Column(String(200))
    camp = db.relationship("TrainCamp", secondary=camp_user)
    #admin = BooleanField()

    def verify_password(self, password):
        return self.password == password

    def __str__(self):
        return self.name + ", " + self.email


class JudgeNorm(db.Model):
    __tablename__ = 'judgenorm'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.TEXT)
    name = db.Column(db.String(200))    
    value = db.Column(db.DECIMAL)

    def  __str__(self):
        return self.name


class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True, index=True)
    train = db.Column(db.String(200))
    test1= db.Column(db.String(200))
    test2 = db.Column(db.String(200))

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class TrainCamp(db.Model):
    __tablename__ = 'traincamp'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True)
    begin_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    user = db.relationship(User, secondary=camp_user)
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

homework_prob = db.Table('homework_prob',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('homework_id', db.ForeignKey('homework.id')),
    db.Column('problem_id', db.ForeignKey('problem.id'))
)


class Problem(db.Model):
    __tablename__ = 'problem'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200))
    data_id = db.Column(db.ForeignKey('data.id'))
    data = db.relationship(Data)
    description = db.Column(db.TEXT)
    judge_id = db.Column(db.ForeignKey('judgenorm.id'))
    judge = db.relationship(JudgeNorm)
    homework = db.relationship("HomeWork", secondary=homework_prob)

    def __str__(self):
        return self.name


class HomeWork(db.Model):
    __tablename__ = 'homework'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    camp_id = db.Column(db.ForeignKey('traincamp.id'))
    camp = db.relationship(TrainCamp)
    name = db.Column(db.String(200))
    #prob_count = IntegerField()
    #submit_count = IntegerField()
    begin_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    problem = db.relationship("Problem", secondary=homework_prob)

    def __str__(self):
        return self.name


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey('user.id'), index=True)
    user = db.relationship(User)
    form = db.Column(ForeignKey('homework_prob.id'))
    score = db.Column(db.Integer)
    source = db.Column(db.TEXT)
    status = db.Column(db.String(10))
    time = db.Column(db.DateTime)