from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from . import main
from .. import app
from .. import Session
from .forms import LoginForm
from ..models import User
from sqlalchemy.orm.exc import NoResultFound

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    sess = Session()
    if form.validate_on_submit():
        try:
            user = sess.query(User).filter(User.email == form.email.data).one()
            if user is not None and user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next') or url_for('main.index'))
        except NoResultFound:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)


@main.route('/index')
def index():
    return render_template('index.html')


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
    try:
        sess.query(User).filter(User.id == user_id).one()
    except NoResultFound:
        return None
