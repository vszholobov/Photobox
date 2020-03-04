from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "97f9fabf1a3d44b2d2e1d9201241ff4k"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

from flask_server import routes, errors, models
