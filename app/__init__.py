from flask import flash, Flask, render_template, redirect, request, url_for
from config import Config
from flask_login import current_user, LoginManager, login_required, login_user, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_moment import Moment
from werkzeug.security import generate_password_hash, check_password_hash

import os
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)
login = LoginManager(app)
csrf = CSRFProtect(app)
moment = Moment(app)
login.login_view = 'login'

from app import routes, models
