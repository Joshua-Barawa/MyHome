from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
import os

app = Flask(__name__)

ENV = os.environ.get("ENV")

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://msfymjupypanwa:017e15df3dbc3b5715be475b57f8400bfef32ee744a18079cf356c92fafedef6@ec2-54-156-110-139.compute-1.amazonaws.com:5432/dfkgqstcrcp5uc"
    app.config['SECRET_KEY'] = "1234567"
    MAIL_SERVER = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'joshua.barawa@student.moringaschool.com'
    app.config['MAIL_PASSWORD'] = 'Mwa2748nda%'
    app.config['MAIL_USE_SSL'] = True
else:
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://projectdb:hello@localhost/projectdb'
    app.config['SECRET_KEY'] = "1234567"
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'joshua.barawa@student.moringaschool.com'
    app.config['MAIL_PASSWORD'] = 'Mwa2748nda%'



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from views import *

manager = Manager(app)
manager.add_command('server', Server)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


login_manager.login_view = 'login'

bcrypt = Bcrypt(app)
mail = Mail(app)

from models import *


@manager.shell
def make_shell_context():
    return dict(db=db, app=app)


if __name__ == '__main__':
    manager.run()
