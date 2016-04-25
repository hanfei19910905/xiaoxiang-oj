from .. import _admin
from flask_admin.contrib.peewee import ModelView
from ..models import *

_admin.add_view(ModelView(User, name="用户管理"))
_admin.add_view(ModelView(TrainCamp, name="训练营管理"))
_admin.add_view(ModelView(HomeWork, name="作业管理"))


class CampUserAdminView(ModelView):
    column_sortable_list = (('训练营', TrainCamp.name), ("学员", User.name))
    column_searchable_list = (User.name, )

_admin.add_view(CampUserAdminView(CampUserRelationShip, name="训练营增删学员"))
_admin.add_view(ModelView(JudgeNorm, name="评价指标"))
_admin.add_view(ModelView(Problem, name="题库"))
_admin.add_view(ModelView(Data, name="数据集管理"))
