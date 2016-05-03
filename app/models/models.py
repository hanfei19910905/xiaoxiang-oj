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
    email = db.Column(db.String(200), unique=True, nullable=False)
    name = db.Column(db.String(200),nullable=False)
    password = db.Column(db.String(200),nullable=False)
    salt = db.Column(db.String(200),nullable=False, default='salt')
    camp = db.relationship("TrainCamp", secondary=camp_user)
    admin = db.Column(db.Boolean(),nullable=False)

    def verify_password(self, password):
        return self.password == password

    @property
    def is_admin(self):
        return self.admin

    def __str__(self):
        return self.name + ", " + self.email


class JudgeNorm(db.Model):
    __tablename__ = 'judgenorm'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200),nullable=False)
    value = db.Column(db.Float)
    code = db.Column(db.String(100),nullable=False)

    def  __str__(self):
        return self.name


class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True, index=True)
    train = db.Column(db.String(200),nullable=False)
    test1= db.Column(db.String(200))
    test2 = db.Column(db.String(200),nullable=False)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class TrainCamp(db.Model):
    __tablename__ = 'traincamp'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True,nullable=False)
    begin_time = db.Column(db.DateTime,nullable=False)
    end_time = db.Column(db.DateTime,nullable=False)
    user = db.relationship(User, secondary=camp_user)

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
    author_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    author = db.relationship(User)
    data_id = db.Column(db.ForeignKey('data.id'), nullable=False)
    data = db.relationship(Data)
    description = db.Column(db.TEXT, nullable=False)
    judge_id = db.Column(db.ForeignKey('judgenorm.id'), nullable=False)
    judge = db.relationship(JudgeNorm)
    homework = db.relationship("HomeWork", secondary=homework_prob)

    def __str__(self):
        return self.name


class HomeWork(db.Model):
    __tablename__ = 'homework'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    camp_id = db.Column(db.ForeignKey('traincamp.id'), nullable=False)
    camp = db.relationship(TrainCamp)
    name = db.Column(db.String(200),nullable=False)
    #prob_count = IntegerField()
    #submit_count = IntegerField()
    begin_time = db.Column(db.DateTime,nullable=False)
    end_time = db.Column(db.DateTime,nullable=False)
    problem = db.relationship("Problem", secondary=homework_prob)

    def __str__(self):
        return self.name


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey('user.id'), index=True)
    user = db.relationship(User)
    prob_id = db.Column(ForeignKey('problem.id'))
    prob = db.relationship(Problem)
    h_id = db.Column(ForeignKey('homework.id'))
    homework = db.relationship(HomeWork)
    score = db.Column(db.Float, default=0)
    # source is the source file path that the student upload
    source = db.Column(db.String(100))
    # result is the result file path that the student upload
    result = db.Column(db.String(100))
    # status
    status = db.Column(db.String(50), default = 'pending')
    # time
    time = db.Column(db.DateTime)


class ProbUserStatic(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey('user.id'))
    prob_id = db.Column(db.ForeignKey('problem.id'))
    score = db.Column(db.Float, default = 0)
