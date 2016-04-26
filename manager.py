import os
from app import app
from app import models
from app import db
from flask_script import Manager
from sandbox import SandBoxService

manager = Manager(app)

@manager.command
def init_db():
    "Initial Database"
    db.drop_all()
    db.create_all()

@manager.command
def sandbox_service(ch):
    print("Arg ch",ch)
    SandBoxService.run(ch)

if __name__ == '__main__':
    manager.run()
