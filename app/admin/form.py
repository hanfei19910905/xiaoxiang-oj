from flask_wtf import Form
from flask_admin.contrib.sqla.fields import QuerySelectField
from ..models import Problem, HomeWork, TrainCamp, IndexSet
from wtforms.validators import DataRequired
from wtforms import SubmitField

def help(_id, cls):
    id = IndexSet.query.filter_by(id = _id).first().set_id
    prob = None
    if id != -1:
        prob = cls.query.filter_by(id = id).first()
    return prob


class IndexSetForm(Form):
    problem = QuerySelectField(label='首页显示题目', query_factory = lambda : Problem.query.all(), validators=[DataRequired(),], default=help(1, Problem))
    homework = QuerySelectField(label='首页显示作业', query_factory = lambda : HomeWork.query.all(), validators=[DataRequired(),], default=help(2, HomeWork))
    traincamp = QuerySelectField(label='首页显示课程', query_factory = lambda : TrainCamp.query.all(), validators=[DataRequired(),], default=help(3, TrainCamp))
    submit = SubmitField('Submit')