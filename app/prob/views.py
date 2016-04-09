#!/usr/bin/env python
# coding=utf-8

from flask import render_template, redirect, request, url_for, flash
from . import prob

@prob.route('/prob')
def prob_view():
    return render_template('prob_view.html')
