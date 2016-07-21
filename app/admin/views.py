import functools
import os
import random
import string

from flask import redirect, url_for, request, flash
from flask_admin import form, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from jinja2 import Markup
from sqlalchemy.event import listens_for
from werkzeug.utils import secure_filename
from wtforms import ValidationError, StringField

from .. import _admin, app
from ..models import *


class SuffixProxy:
    name = ""


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


class PwdField(StringField):
    change = False
    def process_formdata(self, valuelist):
        if valuelist:
            if self.data == valuelist[0]:
                return
            self.change = True
            self.data = valuelist[0]
        else:
            self.data = ""

    def populate_obj(self, obj, name):
        if self.change:
            setattr(obj, name, hashPwd(self.data, obj.salt))


class UserView(ModelView):
    column_filters = ['name', 'email']
    column_editable_list = ['role']
    column_exclude_list = ['salt', 'sub_id']
    form_columns = ['camp', 'name', 'email', 'salt', 'role', 'password']
    form_overrides = {
        'password' : PwdField,
    }
    form_widget_args = {
        'salt' : {
            'readonly' : True
        },
        'sub_id' : {
            'readonly' : True
        },
    }
    form_args = {
        'salt': {
            'default': lambda : ''.join(random.sample(string.ascii_lowercase,4))
        },
    }

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
    column_default_sort = ('id', True)
    form_args = {
        'begin_time':{'validators': [_validate]},
        'end_time':{'validators': [_validate]},
    }

    def is_accessible(self):
        if AdminView.is_accessible(self) and current_user.is_admin:
            return True
        return False


def _query_factory_owner():
    return User.query.filter_by(id = current_user.id).all()


class HomeWorkView(AdminView):
    column_default_sort = ('id', True)
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

    def _query_factory_camp():
        if current_user.is_admin:
            return TrainCamp.query.all()
        else:
            return TrainCamp.query.join(camp_user).filter_by(user_id = current_user.id).all()

    form_args = {
        'begin_time': {'validators': [_validate]},
        'end_time': {'validators': [_validate]},
        'camp': {'query_factory': _query_factory_camp},
        'owner': {'query_factory': _query_factory_owner},
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
        return secure_filename(obj.name + "_judge.py")

    form_overrides = {
        'code': form.FileUploadField,
    }

    form_args = {
        'code' : {'label' : 'Judge Code', 'base_path' : app.config['UPLOAD_FOLDER'], 'allow_overwrite' : false, 'relative_path' : 'judge/', 'namegen' : namegen, "allowed_extensions" : ['py']},
        'owner': {'query_factory': _query_factory_owner},
    }

    def _list_download_link(view, context, model, name):
        return Markup('<a href=/download/%s> download </a>' % (model.code))

    column_formatters = {
        'code': _list_download_link
    }

    def on_model_delete(self, model):
        if current_user.is_admin or (current_user.is_teacher and current_user.id == model.owner.id):
            return
        raise ValidationError("你没有这个权限删除这个指标！")

_admin.add_view(JudgeView(JudgeNorm, db.session, name="指标管理"))


class ProbView(AdminView):
    column_default_sort = ('id', True)
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

    form_args = {
        'author': {'query_factory': _query_factory_owner},
    }

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
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'data/%s_train.%s' % (target.name, target.train[-3:])))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'data/%s_test1.%s' % (target.name, target.test1[-3:])))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'secret/%s_test2.%s' % (target.name, target.test2[-3:])))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'data/%s_attach.%s' % (target.name, target.attach[-3:])))
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass


class DataField(form.FileUploadField):
    def populate_obj(self, obj, name):
        filename = self.generate_name(obj, self.data)
        setattr(obj, name, filename)


suffix_map = {
    "train": SuffixProxy(),
    "attach": SuffixProxy(),
    "test1": SuffixProxy(),
    "test2": SuffixProxy(),
}


def namegen(suffix, obj, _):
    return suffix.name


class DataView(AdminView):
    create_template = 'admin/data_create.html'
    can_edit = False
    suffix = ""
    column_exclude_list = ["uploading"]
    form_columns = ['owner', 'name', 'train', 'attach', 'test1', 'test2']

    def get_query(self):
        return Data.query.filter_by(uploading=False)

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

    filename = ""

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        if request.method == 'GET':
            return AdminView.create_view(self)
        files = request.files
        key = ""
        for _ in files.keys():
            key = _
        value = files[key] # this is a Werkzeug FileStorage object
        name = request.form['name']
        global suffix_map
        suffix = suffix_map[key]
        suffix.name = 'csv'
        print(name, value.filename[-3:])
        if value.filename[-3:] == "zip":
            suffix.name = 'zip'
        print('key!!!', key, suffix, request)
        if 'Content-Range' in request.headers:
            range_str = request.headers['Content-Range'].split(" ")[1]
            left, right_str = range_str.split('-')
            right, all = right_str.split('/')
            left, right, all = int(left), int(right), int(all)
            print(left, right, all)
            if left == 0:
                if name is None or name == "":
                    flash(" 文件名不可以为空！！")
                    return ('', 400)

                if key == 'train' and Data.query.filter_by(name=name).first() is not None:
                    flash("这个文件名已经存在！！")
                    return ('', 400)
                try:
                    if key == 'test2':
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'secret/%s_%s.%s' % (name, key, suffix.name)))
                    else:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'data/%s_%s.%s' % (name, key, suffix.name)))
                except OSError:
                    pass
            if key == 'test2':
                prefix = 'secret/'
            else:
                prefix = 'data/'
            filename = prefix + name + "_" + key + "." + suffix.name
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'ab') as f:
                f.seek(int(left))
                f.write(value.stream.read())
            d = Data.query.filter_by(name=name).first()
            if d is not None:
                setattr(d, key, suffix.name)
                if right + 1 == all:
                    d.uploading = False
                else:
                    d.uploading = True
                db.session.commit()
            if right + 1 == all:
                response = AdminView.create_view(self)
                d = Data.query.filter_by(name=name).first()
                d.uploading = False
                db.session.commit()
                return response
            return ('', 200)
        else:
            # first time
            if name is None or name == "":
                flash(" 文件名不可以为空！！")
                return ('', 400)
            if key == 'train' and Data.query.filter_by(name=name).first() is not None:
                flash(" 请重新命名！！")
                return ('', 400)
            if key == 'test2':
                path = os.path.join(app.config['UPLOAD_FOLDER'], 'secret/%s_%s.%s' % (name, key, suffix.name))
            else:
                path = os.path.join(app.config['UPLOAD_FOLDER'], 'data/%s_%s.%s' % (name, key, suffix.name))
            try:
                os.remove(path)
            except OSError:
                # Don't care if was not deleted because it does not exist
                pass
            d = Data.query.filter_by(name=name).first()
            if d is not None:
                setattr(d, key, suffix.name)
                if key == 'attach':
                    d.uploading = False
                db.session.commit()
            value.save(path)
            return AdminView.create_view(self)

    form_overrides = {
        'train' : DataField,
        'test1' : DataField,
        'test2' : DataField,
        'attach' : DataField,
    }

    form_args = {
        'train': {'label': 'Train File', 'namegen': functools.partial(namegen, suffix_map['train'])},
        'test1': {'label': 'Test1 File', 'namegen': functools.partial(namegen, suffix_map['test1'])},
        'attach': {'label': 'Attachment File', 'namegen': functools.partial(namegen, suffix_map['attach'])},
        'test2': {'label': 'Test2 File', 'namegen': functools.partial(namegen, suffix_map['test2'])},
        'owner': {'query_factory': _query_factory_owner},
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

    def _list_download_link (view, context, model, name):
        filename =''
        if name == 'train':
            filename = 'data/' + model.name + "_train"
        elif name == 'test1':
            filename = 'data/' + model.name + "_test1"
        elif name == 'test2':
            filename = 'secret/' + model.name + "_test2"
        elif name == 'attach':
            filename = 'data/' + model.name + "_attach"

        return Markup('<a href=/download/%s> download </a>' % (filename))

    column_formatters = {
        'train': _list_download_link,
        'test1': _list_download_link,
        'test2': _list_download_link,
        'attach':_list_download_link,
    }
_admin.add_view(DataView(Data, db.session, name="数据集管理"))


class SubView(AdminView):
    can_delete = False
    can_create = False
    page_size = 50
    can_edit = False
    column_default_sort = ('id', True)
    column_filters = ['user.name', 'homework.name', 'prob.name', 'status']
    list_template = 'admin/myList.html'
    column_exclude_list = ["result"]

    def get_query(self):
        if current_user.is_admin:
            return Submission.query
        elif current_user.is_teacher:
            return Submission.query.join(HomeWork).join(TrainCamp).filter(or_(HomeWork.owner_id == current_user.id, TrainCamp.public == True))
        else:
            return None

    def _show_result(view, context, model, name):
        return Markup('<a data-toggle="modal" href="/download/show/%s" data-target="#%s">显示代码</a>' % ( str(model.id),  str(model.id)))

    column_formatters= {
        'source': _show_result,
    }

_admin.add_view(SubView(Submission, db.session, name="提交记录查看"))

class IndexSetView(AdminView):
    can_create = False
    can_delete = False
    can_edit = False

    def is_accessible(self):
        if AdminView.is_accessible(self) and current_user.is_admin:
            return True
        return False

    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        from .form import IndexSetForm
        form = IndexSetForm()
        if form.validate_on_submit() :
            problem = form.problem
            homework = form.homework
            traincamp = form.traincamp

            li = IndexSet.query.all()
            li[0].set_id  = problem.data.id
            li[1].set_id  = homework.data.id
            li[2].set_id  = traincamp.data.id
            db.session.commit()
            flash('更新成功！')
            return redirect('/admin/indexset')

        return self.render('admin/index_set.html', form=form)

_admin.add_view(IndexSetView(IndexSet, db.session, name="首页配置"))
