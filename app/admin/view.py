from .. import _admin, db, app
from flask_admin.contrib.sqla import ModelView
from flask_admin import form
from jinja2 import Markup
from ..models import *

_admin.add_view(ModelView(User,  db.session, name="用户管理"))
_admin.add_view(ModelView(TrainCamp, db.session, name="训练营管理"))
_admin.add_view(ModelView(HomeWork, db.session, name="作业管理"))
_admin.add_view(ModelView(JudgeNorm, db.session, name="评价指标"))
_admin.add_view(ModelView(Problem, db.session, name="题库"))


class DataView(ModelView):
    form_overrides = {
        'train' : form.FileUploadField,
        'test1' : form.FileUploadField,
        'test2' : form.FileUploadField,
    }

    form_args = {
        'train' : {'label' : 'Train File', 'base_path' : app.config['UPLOAD_FOLDER']},
        'test1' : {'label' : 'Test File1', 'base_path' : app.config['UPLOAD_FOLDER']},
        'test2' : {'label' : 'Test File2', 'base_path' : app.config['UPLOAD_FOLDER']},
    }

    def _list_download_link(view, context, model, name):
        filename =''
        if name == 'train':
            filename = model.train
        elif name == 'test1':
            filename = model.test1
        elif name == 'test2':
            filename = model.test2

        return Markup('<a href="/download/%s"> download </a>' % filename)

    column_formatters = {
        'train': _list_download_link,
        'test1': _list_download_link,
        'test2': _list_download_link,
    }
_admin.add_view(DataView(Data, db.session, name="数据集管理"))

print(app.config['UPLOAD_FOLDER'])
