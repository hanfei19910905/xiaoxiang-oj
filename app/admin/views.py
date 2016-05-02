from .. import _admin, db, app
from flask import redirect, url_for, request, flash
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from sqlalchemy.event import listens_for
from flask_admin import form
from jinja2 import Markup
from ..models import *
import functools, os


class AdminView(ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.is_admin:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        flash('you are not logined as admin!!')
        return redirect(url_for('main.login', next = request.url))


_admin.add_view(AdminView(User,  db.session, name="用户管理"))
_admin.add_view(AdminView(TrainCamp, db.session, name="训练营管理"))
_admin.add_view(AdminView(HomeWork, db.session, name="作业管理"))


class JudgeView(AdminView):
    def namegen(obj, filedata):
        try:
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'judge', obj.name))
        except os.error:
            print('error!!')
        return obj.name + "/judge.py"

    form_overrides = {
        'code': form.FileUploadField,
    }

    form_args = {
        'code' : {'label' : 'Judge Code', 'base_path' : app.config['UPLOAD_FOLDER'], 'allow_overwrite' : false, 'relative_path' : 'judge/', 'namegen' : namegen, "allowed_extensions" : ['py']},
    }

    def _list_download_link(view, context, model, name):
        return Markup('<a href=/download/%s> download </a>' % (model.code))

    column_formatters = {
        'code': _list_download_link
    }

_admin.add_view(JudgeView(JudgeNorm, db.session, name="评价指标"))
_admin.add_view(AdminView(Problem, db.session, name="题库"))


@listens_for(Data, 'after_delete')
def del_path(mapper, conn, target):
    if target.name:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'data/%s_train' % target.name))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'data/%s_test1' % target.name))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'secret/%s_test2' % target.name))
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass


@listens_for(Submission, 'after_delete')
def del_path(mapper, conn, target):
    if target.id:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'submission/%s/source' % target.id))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'submission/%s/result' % target.id))
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass


class DataView(AdminView):
    def namegen(filename, obj, filedata):
        return obj.name + "_" + filename


    form_overrides = {
        'train' : form.FileUploadField,
        'test1' : form.FileUploadField,
        'test2' : form.FileUploadField,
    }

    form_args = {
        'train' : {'label' : 'Train File', 'base_path' : app.config['UPLOAD_FOLDER'], 'allow_overwrite' : false, 'relative_path' : 'data/', 'namegen' : functools.partial(namegen, 'train')},
        'test1' : {'label' : 'Test1 File', 'base_path' : app.config['UPLOAD_FOLDER'], 'allow_overwrite' : false, 'relative_path' : 'data/', 'namegen' : functools.partial(namegen, 'test1')},
        'test2' : {'label' : 'Test2 File', 'base_path' : app.config['UPLOAD_FOLDER'], 'allow_overwrite' : false, 'relative_path' : 'secret/', 'namegen' : functools.partial(namegen, 'test2')},
    }

    def _list_download_link(view, context, model, name):
        filename =''
        if name == 'train':
            filename = model.train
        elif name == 'test1':
            filename = model.test1
        elif name == 'test2':
            filename = model.test2

        return Markup('<a href=/download/%s> download </a>' % (filename))

    column_formatters = {
        'train': _list_download_link,
        'test1': _list_download_link,
        'test2': _list_download_link,
    }
_admin.add_view(DataView(Data, db.session, name="数据集管理"))

