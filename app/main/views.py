from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from . import main
from .. import db, login_manager
from .forms import LoginForm
from ..models import User, Submission, Problem, HomeWork, TrainCamp, ProbUserStatic, homework_prob, IndexSet
from sqlalchemy import func


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form, active = 'Login')


@main.route('/index')
def index():
    return render_template('index.html', active='index')


@main.route('/')
def index1():
    return redirect(url_for('main.index'))


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@main.route('/rank/<rname>', methods=['GET', 'POST'])
def get_rank(rname=None):
    id_li = IndexSet.query.all()
    pid = id_li[0].set_id
    sub_list = ProbUserStatic.query.filter_by(prob_id = pid).all()
    if len(sub_list) <= 0:
        return render_template('ranklist.html')
    prob = Problem.query.filter_by(id = pid).first()
    plist = [prob]
    prank = dict()
    for sub in sub_list:
        uname = User.query.filter_by(id = sub.user_id).one().name
        if uname not in prank:
            prank[uname] = dict()
            prank[uname][pid] = '没有得分'
        prank[uname][sub.prob_id] = sub.score
    prlist = sorted(prank.items(), key=lambda d:d[1][pid], reverse= not prob.judge.desc)
    sub_list2 = db.session.query(func.max(Submission.score),
        Submission.prob_id, Submission.h_id, Submission.user_id)\
        .group_by(Submission.h_id, Submission.prob_id, Submission.user_id).all()
    clist = TrainCamp.query.filter_by(id = id_li[2].set_id).all()
    hlist = HomeWork.query.filter_by(id = id_li[1].set_id).all()
    if len(sub_list2) <= 0:
        return render_template('ranklist.html')
    crank = dict()
    hrank = dict()
    for sub in sub_list2:
        if sub.h_id is None:
            continue
        uname = User.query.filter_by(id=sub[3]).one().name
        if uname not in hrank:
            hrank[uname] = dict()
            for h in hlist:
                hrank[uname][h.id] = 0.0
        if uname not in crank:
            crank[uname] = dict()
            for c in clist:
                crank[uname][c.id] = 0.0
        hkey = sub[2]
        hrank[uname][sub[2]] += float(sub[0])
        home = HomeWork.query.filter_by(id = sub.h_id).one()
        ckey = home.camp_id
        crank[uname][home.camp_id] += float(sub[0])
    hrlist = sorted(hrank.items(),key= lambda d:d[1][hkey], reverse=True)
    crlist = sorted(crank.items(),key= lambda d:d[1][ckey], reverse=True)
    if rname == 'prob':
        res = prlist
        rlist = plist
    elif rname == 'home':
        res = hrlist
        rlist = hlist
    else:
        res = crlist
        rlist = clist
    return render_template('ranklist.html', prank=res, plist=rlist, type=rname)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
