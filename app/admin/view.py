from .. import _admin
from flask_admin.contrib.peewee import ModelView
from ..models import *

_admin.add_view(ModelView(User))
#_admin.add_view(ModelView(Contest))
_admin.add_view(ModelView(Problem))
_admin.add_view(ModelView(Judge_way))
_admin.add_view(ModelView(Submission))