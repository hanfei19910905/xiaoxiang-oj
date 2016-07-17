#!/usr/bin/env python
# coding=utf-8

from flask import render_template, redirect, url_for, flash, request
from . import prob
from .. import app, db
from .forms import SubmitForm
from ..models import Problem, Submission, User, ProbUserStatic
from flask_login import login_required, current_user
import datetime, os
from sandbox import async_call
from sqlalchemy import func

@prob.route('/problem_set') 
def prob_set():
    plist = Problem.query.order_by(Problem.id.desc()).all()
    return render_template('prob_list.html', plist=plist, active='problem')


def checkValid(hid, pid):
    problem = Problem.query.filter_by(id = pid).first()
    homework = None
    home_list = problem.homework
    for home in home_list:
        if int(home.id) == hid:
            homework = home
            if not homework.camp.public and not current_user.is_admin :
                valid = False
                for user in home.camp.user:
                    if user.id == current_user.id:
                        valid = True
                        break
                if not valid:
                    flash('你没有权限提交这个作业！')
                    return redirect(request.args.get('next') or url_for("main.index")), False, problem, homework
            break
    return None, True, problem, homework


def clear_env():
    current_user.sub_id = -1
    db.session.commit()


@prob.route('/problem_set/<hid>/<pid>', methods=['GET', 'POST'])
@login_required
def prob_view(hid, pid):
    hid = int(hid)
    pid = int(pid)
    if request.method  == 'GET':
        return prob_view_get(hid, pid)
    else:
        files = request.files
        key = ""
        for _ in files.keys():
            key = _
        value = files[key] # this is a Werkzeug FileStorage object
        print("get!! filename: " + key + " current_user %d" % current_user.id)
        print(request.headers)
        if 'Content-Range' in request.headers:
            if key == 'result':
                id = current_user.sub_id
                if id != -1:
                    range_str = request.headers['Content-Range'].split(" ")[1]
                    left, right_str = range_str.split('-')
                    right, all = right_str.split('/')
                    left, right, all = int(left), int(right), int(all)
                    print("range! %d %d %d subId: %d" % (left, right, all, id))
                    submission_path = os.path.join(app.config['UPLOAD_FOLDER'], 'submission', str(id), 'result.csv')
                    if left == 0: # clear path
                        try :
                            os.remove(submission_path)
                        except:
                            pass
                    with open(submission_path, 'ab') as f:
                        f.write(value.stream.read())
                    if right + 1 == all:
                        print('success', id)
                        flash("提交成功")
                        clear_env()
                        sub = Submission.query.filter_by(id = id).first()
                        if sub is None:
                            flash('unkown error!')
                            app.logger.error("so sad!!! unknown id!! %d", sub)
                            return redirect(request.args.get('next') or url_for("main.index"))
                        problem = sub.prob
                        #todo: check if it is a zip file.
                        app.logger.info("call!! %s" % str(id))
                        async_call.delay(id, os.path.join(app.config['UPLOAD_FOLDER'], 'submission', str(id), 'result.csv'),
                                            os.path.join(app.config['UPLOAD_FOLDER'], problem.data.test2),
                                            os.path.join(app.config['UPLOAD_FOLDER'], problem.judge.code))
                        sub.status = 'queueing...'
                        db.session.commit()
                        return redirect(url_for('prob.status'))
                    else:
                        return ("", 200)
                err = '未知错误！'
            else:
                err = '源文件大小不可以超过1MB!!'
            flash(err)
            clear_env()
            return redirect(url_for('prob.prob_view', hid = hid, pid = pid))
        elif key == "source":
            # first check
            result, ok, problem, homework = checkValid(hid, pid)
            if not ok :
                app.logger.error("source is not valid!")
                return result
            form = SubmitForm()
            if form.validate_on_submit() and problem is not None and homework is not None:
                src_ext = value.filename.rsplit('.', 1)[-1]
                if homework.begin_time < datetime.datetime.now() < homework.end_time:
                    sub = Submission(user_id = current_user.id, h_id = hid, prob_id = pid, source = src_ext, result = "", time = datetime.datetime.now(), status = 'pending')
                else:
                    app.logger.error("out of date!")
                    flash('the homework is out of date!')
                    return redirect(request.args.get('next') or url_for("main.index"))
                db.session.add(sub)
                db.session.commit()
                app.logger.info("create sub %d!" % sub.id)
                try:
                    submission_path = os.path.join(app.config['UPLOAD_FOLDER'], 'submission', str(sub.id))
                    os.makedirs(submission_path)
                    app.logger.info("path: %s" % submission_path)
                    if src_ext =='py':
                        value.save(os.path.join(submission_path, 'source.py'))
                    else:
                        value.save(os.path.join(submission_path, value.filename))
                        cmd= "unzip %s -d %s" % (os.path.join(submission_path, value.filename), submission_path)
                        ret = os.system(cmd)
                        if ret != 0:
                            flash('unzip failed!'  + cmd)
                            db.session.delete(sub)
                            db.session.commit()
                            return redirect(request.args.get('next') or url_for("main.index"))
                except os.error:
                    flash('save source file failed! err is ', os.error.strerror)
                    app.logger.error('save source file failed! err is ', os.error.strerror)
                    db.session.delete(sub)
                    db.session.commit()
                    return redirect(request.args.get('next') or url_for("main.index"))
                current_user.sub_id = sub.id
                db.session.commit()
                return ("", 200)
            else:
                flash('非法的提交！')
                return redirect(request.args.get('next') or url_for("main.index"))
        else:
            id = current_user.sub_id
            if id != -1:
                sub = Submission.query.filter_by(id = id).first()
                if sub is None:
                    app.logger.error("can't find sid")
                    flash('unknown error!')
                    return redirect(request.args.get('next') or url_for("main.index"))
                problem = sub.prob
                submission_path = os.path.join(app.config['UPLOAD_FOLDER'], 'submission', str(id), 'result.csv')
                value.save(submission_path)
                app.logger.info("call!! %s" % str(id))
                async_call.delay(id, os.path.join(app.config['UPLOAD_FOLDER'], 'submission', str(id), 'result.csv'),
                                    os.path.join(app.config['UPLOAD_FOLDER'], problem.data.test2),
                                    os.path.join(app.config['UPLOAD_FOLDER'], problem.judge.code))
                flash("提交成功")
                clear_env()
                return redirect(url_for('prob.status'))
            flash("未知错误")
            clear_env()
            return redirect(url_for('prob.prob_view', hid = hid, pid = pid))


def prob_view_get(hid, pid):
    result, ok, problem, homework = checkValid(hid, pid)
    if not ok:
        return result
    form = SubmitForm()
    plist = ['rank', 'user name', problem.name, 'Entries', 'last submit time']
    result = db.session.query(ProbUserStatic.user_id, func.sum(ProbUserStatic.real_score), func.max(ProbUserStatic.score), func.sum(ProbUserStatic.submit_times), func.max(ProbUserStatic.last_time)). \
        filter(ProbUserStatic.prob_id == problem.id, ProbUserStatic.score > 0) \
        .group_by(ProbUserStatic.user_id).order_by(func.sum(ProbUserStatic.real_score)).all()
    prank = []
    for i, res in enumerate(result):
        name = User.query.filter_by(id=res[0]).first().name
        prank.append([i + 1, name, res[2], res[3], res[4]])
    if hid == -1:
        return render_template('prob_view.html', problem=problem, form=form, hid=-1, data=problem.data, active='problem', attach = False, plist = plist, prank = prank)
    attach = os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], problem.data.attach))
    return render_template('prob_view.html', problem=problem, form=form, hid=hid, data=problem.data, active='homework', attach =attach, plist = plist, prank = prank)


@prob.route('/status')
@login_required
def status():
    submission_set = Submission.query.filter_by(user_id = current_user.get_id()).order_by(Submission.id.desc()).all()
    return render_template("status.html", slist = submission_set, active='status')
