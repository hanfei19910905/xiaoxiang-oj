#!/usr/bin/env python
# coding=utf-8

from .. import db
from peewee import *
from flask import render_template, redirect, request, url_for, flash
from . import contest
from ..models import Contest

@contest.route('/clist')
def clist_view():
    return render_template('contest_list.html')