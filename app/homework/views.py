#!/usr/bin/env python
# coding=utf-8

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required
from . import homework
from ..models import HomeWork, homework_prob
import datetime
from sqlalchemy.orm.exc import NoResultFound


@homework.route('/list')
@login_required
def list_view():
    try:
        hlist = HomeWork.query.order_by(HomeWork.begin_time.desc()).all()
        return render_template('homework_list.html', clist=hlist, active = 'homework')
    except NoResultFound:
        flash('什么作业都没有哦')
    return redirect(url_for('main.index'))


@homework.route('/problist/<hid>')
@login_required
def contest_view(hid):
    contest = HomeWork.query.filter_by(id = hid).first()
    if contest is None or contest.begin_time > datetime.datetime.now() or datetime.datetime.now() > contest.end_time:
        flash("这个作业不在时间内！")
        return redirect(url_for('main.index'))
    plist = contest.problem
    plist = sorted(plist, key=lambda x:x.id, reverse=True)
    return render_template('contest_view.html', plist=plist, homework=contest, active = 'homework')
