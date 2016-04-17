#!/usr/bin/env python
# coding=utf-8

from flask import Blueprint

prob = Blueprint('prob', __name__, template_folder="../templates")

from sandbox import SandBoxRpcClient

sandbox_client = SandBoxRpcClient("Judger1")

from . import views
