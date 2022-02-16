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
    app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://cjoaetrddihslj:47e396a936a9ab38bf0bde7719b9f5d45820351c863a1fc4096cb5f5524bee44@ec2-54-235-98-1.compute-1.amazonaws.com:5432/d4emr3uvb60cv"
    app.config['SECRET_KEY'] = "1234567"

else:
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://projectdb:hello@localhost/projectdb'
    app.config['SECRET_KEY'] = "1234567"


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



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
from views import *
from models import *


@manager.shell
def make_shell_context():
    return dict(db=db, app=app)


if __name__ == '__main__':
    manager.run()
