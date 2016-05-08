from flask import render_template, redirect, request, url_for, flash, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from . import main
from .. import app
from .. import Session
from .. import db
from .forms import LoginForm
from ..models import User, Submission, Problem, HomeWork, TrainCamp, ProbUserStatic
from sqlalchemy.orm.exc import NoResultFound
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
    sub_list = ProbUserStatic.query.all()
    if len(sub_list) <= 0:
        return render_template('index.html', active='index')
    plist = db.session.query(Problem).all()
    prank = dict()
    for sub in sub_list:
        uname = User.query.filter_by(id = sub.user_id).one().name
        if uname not in prank:
            prank[uname] = dict()
            for prob in plist:
                prank[uname][prob.id] = '没有得分'
            prank[uname]['total'] = 0
        prank[uname][sub.prob_id] = sub.score
        prank[uname]['total'] += sub.score
    prlist = sorted(prank.items(), key=lambda d:d[1]['total'], reverse=True)
    sub_list2 = db.session.query(func.max(Submission.score), \
        Submission.prob_id, Submission.h_id, Submission.user_id)\
        .group_by(Submission.h_id, Submission.prob_id, Submission.user_id).all()
    crank = dict()
    clist = db.session.query(TrainCamp).all()
    hrank = dict()
    hlist = db.session.query(HomeWork).all()
    for sub in sub_list2:
        if sub.h_id is None:
            continue
        uname = User.query.filter_by(id=sub[3]).one().name
        if uname not in hrank:
            hrank[uname] = dict()
            for h in hlist:
                hrank[uname][h.id] = 0.0
            hrank[uname]['total'] = 0.0
        if uname not in crank:
            crank[uname] = dict()
            for c in clist:
                crank[uname][c.id] = 0.0
            crank[uname]['total'] = 0.0
        hrank[uname][sub[2]] += float(sub[0])
        hrank[uname]['total'] += float(sub[0])
        crank[uname]['total'] += float(sub[0])
        home = HomeWork.query.filter_by(id = sub.h_id).one()
        crank[uname][home.camp_id] += float(sub[0])
    try:
        hrlist = sorted(hrank.items(), key=lambda d:d[1]['total'], reverse=True)
        crlist = sorted(crank.items(), key=lambda d:d[1]['total'], reverse=True)
    except KeyError:
        return render_template('index.html', prank=prlist, active= 'index')
    return render_template('index.html', prank=prlist, hrank=hrlist, crank=crlist, plist = plist, hlist = hlist, clist = clist,  active='index')

@main.route('/')
def index1():
    return redirect(url_for('main.index'))


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

from .. import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

