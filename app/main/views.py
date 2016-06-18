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

    if rname == 'prob':
        prob_list = Problem.query.filter_by(id = id_li[0].set_id).all()
        if len(prob_list) == 0:
            return render_template('ranklist.html')
        title_list = ['rank', 'user name', prob_list[0].name, 'Entries', 'last submit time']
    elif rname == 'home':
        prob_list = Problem.query.filter(Problem.homework.any(id = id_li[1].set_id)).all()
        if len(prob_list) == 0:
            return render_template('ranklist.html')
        title_list = ['rank', 'user name', HomeWork.query.filter_by(id = id_li[1].set_id).first().name, 'Entries', 'last submit time']
    else:
        prob_list = Problem.query.filter(Problem.homework.any(camp_id = id_li[2].set_id)).all()
        if len(prob_list) == 0:
            return render_template('ranklist.html')
        title_list = ['rank', 'user name', TrainCamp.query.filter_by(id = id_li[1].set_id).first().name, 'Entries', 'last submit time']
    result = db.session.query(ProbUserStatic.user_id, func.sum(ProbUserStatic.real_score), func.max(ProbUserStatic.score), func.sum(ProbUserStatic.submit_times), func.max(ProbUserStatic.last_time)).\
        filter(ProbUserStatic.prob_id.in_(tuple(map( lambda prob: prob.id, prob_list))), ProbUserStatic.score > 0)\
        .group_by(ProbUserStatic.user_id).order_by(func.sum(ProbUserStatic.real_score)).all()
    if len(result) == 0:
        return render_template('ranklist.html')
    result = reversed(result)
    prank = []
    for i, res in enumerate(result) :
        name = User.query.filter_by(id=res[0]).first().name
        if rname == 'prob':
            prank.append([i + 1, name, res[2], res[3], res[4]])
        else:
            prank.append([i + 1, name, round(res[1], 6), res[3], res[4]])
    return render_template('ranklist.html', prank=prank, plist=title_list)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
