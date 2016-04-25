from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from . import main
from .. import app
from .forms import LoginForm
from ..models import User
from peewee import DoesNotExist


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.select().where(User.email == form.email.data).get()
            if user is not None and user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next') or url_for('main.index'))
        except DoesNotExist:
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
        User.select().where(User.id == user_id).get()
    except DoesNotExist:
        return None
