from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_wtf import Form
from wtforms import SubmitField
from wtforms.validators import DataRequired

from ..models import Problem, HomeWork, TrainCamp, IndexSet


def help(_id, cls):
    id = IndexSet.query.filter_by(id = _id).first().set_id
    prob = None
    if id != -1:
        prob = cls.query.filter_by(id = id).first()
    return prob


def query_fac(cls):
    li = cls.query.all()
    li.append(cls(id=-1, name="None"))
    return li


class IndexSetForm(Form):
    problem = QuerySelectField(label='首页显示题目', query_factory=lambda: query_fac(Problem), validators=[DataRequired(), ],
                               default=help(1, Problem))
    homework = QuerySelectField(label='首页显示作业', query_factory=lambda: query_fac(HomeWork),
                                validators=[DataRequired(), ], default=help(2, HomeWork))
    traincamp = QuerySelectField(label='首页显示课程', query_factory=lambda: query_fac(TrainCamp),
                                 validators=[DataRequired(), ], default=help(3, TrainCamp))
    submit = SubmitField('Submit')