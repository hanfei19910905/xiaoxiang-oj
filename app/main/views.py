from flask import render_template, redirect, request, url_for, flash, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from . import main
from .. import app
from .. import Session
from .. import db
from .forms import LoginForm
from ..models import User, Submission, Problem, HomeWork
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
    return render_template('login.html', form=form)


@main.route('/index')
def index():
    sub_list = db.session.query(func.max(Submission.score), Submission.user_id, Submission.prob_id) \
               .group_by(Submission.prob_id, Submission.user_id).all()
    plist = db.session.query(Problem).all()
    prank = dict()
    for sub in sub_list:
        uname = User.query.filter_by(id = sub[1]).one().name
        if uname not in prank:
            prank[uname] = dict()
            for prob in plist:
                prank[uname][prob.id] = 0
            prank[uname]['total'] = 0.0
        prank[uname][sub[2]] = float(sub[0])
        prank[uname]['total'] += float(sub[0])
    prlist = sorted(prank.items(), key=lambda d:d[1]['total'], reverse=True)
    sub_list2 = db.session.query(func.max(Submission.score), \
        Submission.prob_id, Submission.h_id, Submission.user_id)\
        .group_by(Submission.h_id, Submission.prob_id, Submission.user_id).all()
    hrank = dict()
    hlist = db.session.query(HomeWork).all()
    for sub in sub_list2:
        uname = User.query.filter_by(id=sub[3]).one().name
        if uname not in hrank:
            hrank[uname] = dict()
            for h in hlist:
                hrank[uname][h.id] = 0.0
            hrank[uname]['total'] = 0.0
        hrank[uname][sub[2]] += float(sub[0])
        hrank[uname]['total'] += float(sub[0])
    hrlist = sorted(hrank.items(), key=lambda d:d[1]['total'], reverse=True)
    return render_template('index.html', prank=prlist, hrank=hrlist)


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

