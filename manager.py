import os
from app import app
from app import models
from flask_script import Manager
from sandbox import SandBoxService

manager = Manager(app)

@manager.command
def init_db():
    "Initial Database"
    m = models.models
    if not m.User.table_exists():
        print("Table user has been created!")
        m.User.create_table()
    if not m.Data.table_exists():
        m.Data.create_table()
    if not m.TrainCamp.table_exists():
        m.TrainCamp.create_table()
    if not m.HomeWork.table_exists():
        m.HomeWork.create_table()
    if not m.JudgeNorm.table_exists():
        m.JudgeNorm.create_table()
    if not m.Problem.table_exists():
        m.Problem.create_table()
    if not m.HomeWorkProbRelationShip.table_exists():
        m.HomeWorkProbRelationShip.create_table()
    if not m.CampUserRelationShip.table_exists():
        m.CampUserRelationShip.create_table()
    if not m.Submission.table_exists():
        m.Submission.create_table()

@manager.command
def sandbox_service(ch):
    print("Arg ch",ch)
    SandBoxService.run(ch)

if __name__ == '__main__':
    manager.run()
