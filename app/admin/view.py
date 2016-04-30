from .. import _admin, db
from flask_admin.contrib.sqla import ModelView
from ..models import *

_admin.add_view(ModelView(User,  db.session, name="用户管理"))
_admin.add_view(ModelView(TrainCamp, db.session, name="训练营管理"))
_admin.add_view(ModelView(HomeWork, db.session, name="作业管理"))
_admin.add_view(ModelView(JudgeNorm, db.session, name="评价指标"))
_admin.add_view(ModelView(Problem, db.session, name="题库"))
_admin.add_view(ModelView(Data, db.session, name="数据集管理"))
