from .. import _admin, db, app
from flask import redirect, url_for, request, flash
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from sqlalchemy.event import listens_for
from flask_admin import form, expose
from wtforms import ValidationError
from jinja2 import Markup
from ..models import *
import functools, os


class AdminView(ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.is_admin or current_user.is_teacher:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        flash('you are not logined as admin!!')
        return redirect(url_for('main.login', next = request.url))


class UserView(ModelView):
    def is_accessible(self):
        if AdminView.is_accessible(self) and current_user.is_admin:
            return True
        return False


_admin.add_view(UserView(User,  db.session, name="用户管理"))


def _validate(form, field):
    if form.begin_time is not None and form.end_time is not None:
        print ('time!!',form.begin_time.data, form.end_time.data)
        if form.begin_time.data >= form.end_time.data:
            raise ValidationError('begin_time must be early than end_time!!')


class TrainCampView(AdminView):
    form_args = {
        'begin_time':{'validators': [_validate]},
        'end_time':{'validators': [_validate]},
    }

    def is_accessible(self):
        if AdminView.is_accessible(self) and current_user.is_admin:
            return True
        return False


class HomeWorkView(AdminView):
    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        id = request.args.getlist('id')[0]
        if id is None:
            return redirect('/admin')
        model = self.get_one(id)
        if not current_user.is_admin and model.owner.id != current_user.id:
            flash('你没有权限编辑！')
            return redirect('/admin')
        return AdminView.edit_view(self)

    def _query_factory():
        if current_user.is_admin:
            return TrainCamp.query.all()
        else:
            return TrainCamp.query.join(camp_user).filter_by(user_id = current_user.id).all()

    form_args = {
        'begin_time': {'validators': [_validate]},
        'end_time': {'validators': [_validate]},
        'camp': {'query_factory': _query_factory},
    }

    def on_model_delete(self, model):
        if current_user.is_admin or (current_user.is_teacher and current_user.id == model.owner.id):
            return
        raise ValidationError("你没有这个权限删除这个指标！")

_admin.add_view(TrainCampView(TrainCamp, db.session, name="课程管理"))
_admin.add_view(HomeWorkView(HomeWork, db.session, name="作业管理"))


class JudgeView(AdminView):
    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        id = request.args.getlist('id')[0]
        if id is None:
            return redirect('/admin')
        model = self.get_one(id)
        if not current_user.is_admin and model.owner.id != current_user.id:
            flash('你没有权限编辑！')
            return redirect('/admin')
        return AdminView.edit_view(self)

    def namegen(obj, filedata):
        return obj.name + "_judge.py"

    form_overrides = {
        'code': form.FileUploadField,
    }

    form_args = {
        'code' : {'label' : 'Judge Code', 'base_path' : app.config['UPLOAD_FOLDER'], 'allow_overwrite' : false, 'relative_path' : 'judge/', 'namegen' : namegen, "allowed_extensions" : ['py']},
    }

    def _list_download_link(view, context, model, name):
        return Markup('<a href=/download/judge/%s> download </a>' % (model.code))

    column_formatters = {
        'code': _list_download_link
    }

    def on_model_delete(self, model):
        if current_user.is_admin or (current_user.is_teacher and current_user.id == model.owner.id):
            return
        raise ValidationError("你没有这个权限删除这个指标！")

_admin.add_view(JudgeView(JudgeNorm, db.session, name="指标管理"))


class ProbView(AdminView):
    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        id = request.args.getlist('id')[0]
        if id is None:
            return redirect('/admin')
        model = self.get_one(id)
        if not current_user.is_admin and model.author.id != current_user.id:
            flash('你没有权限编辑！')
            return redirect('/admin')
        return AdminView.edit_view(self)

    column_exclude_list = form_excluded_columns = ['homework', 'ac_count', 'submit_count']
    page_size = 50
    list_template = 'admin/myList.html'

    def _show_result(view, context, model, name):
        return Markup('<a data-toggle="modal" href="/download/show_prob/%s" data-target="#%s">Show Problem</a>' % (str(model.id), str(model.id)))

    column_formatters= {
        'description': _show_result,
    }

    def on_model_delete(self, model):
        if current_user.is_admin or (current_user.is_teacher and current_user.id == model.author.id):
            return
        raise ValidationError("你没有这个权限删除这个指标！")

_admin.add_view(ProbView(Problem, db.session, name="题库"))


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
    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        id = request.args.getlist('id')[0]
        if id is None:
            return redirect('/admin')
        model = self.get_one(id)
        if not current_user.is_admin and model.owner.id != current_user.id:
            flash('你没有权限编辑！')
            return redirect('/admin')
        return AdminView.edit_view(self)

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

    def on_model_change(self, form, model, is_created):
        if current_user.is_admin or (current_user.is_teacher and current_user.id == model.owner.id):
            return
        if is_created:
            raise ValidationError("你没有权限创建不属于自己的数据集！")
        else:
            raise ValidationError("你没有权限更新不属于自己的数据集！")

    def on_model_delete(self, model):
        if current_user.is_admin or (current_user.is_teacher and current_user.id == model.owner.id):
            return
        raise ValidationError("你没有这个权限删除这个数据集！")

    def _list_download_link(view, context, model, name):
        filename =''
        if name == 'train':
            filename = model.train
        elif name == 'test1':
            filename = model.test1
        elif name == 'test2':
            filename = model.test2

        return Markup('<a href=/download/data/%s> download </a>' % (filename))

    column_formatters = {
        'train': _list_download_link,
        'test1': _list_download_link,
        'test2': _list_download_link,
    }
_admin.add_view(DataView(Data, db.session, name="数据集管理"))


class SubView(AdminView):
    can_delete = False
    can_create = False
    page_size = 50
    can_edit = False
    column_filters = ['user.name', 'homework.name', 'prob.name', 'status']
    list_template = 'admin/myList.html'

    def _show_result(view, context, model, name):
        return Markup('<a data-toggle="modal" href="/download/show/%s" data-target="#%s">显示代码</a>' % ( str(model.id),  str(model.id)))

    column_formatters= {
        'source': _show_result,
    }

_admin.add_view(SubView(Submission, db.session, name="提交记录查看"))