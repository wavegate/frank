from app import db, login
from flask_login import current_user, LoginManager, login_required, login_user, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='author', lazy='dynamic')
    weights = db.relationship('Weight', backref='author', lazy='dynamic')
    tests = db.relationship('Test', backref='author', lazy='dynamic')
    current_task_id = db.Column(db.Integer)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    notes = db.Column(db.String(5000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    complete = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime, default=datetime.now)
    deadline = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    location = db.Column(db.String(140))
    isEvent = db.Column(db.Boolean, default=False)
    stashed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Task {}>'.format(self.title)

class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Weight {}>'.format(self.value)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    testname = db.Column(db.String(140))
    score = db.Column(db.String(140))
    accuracy = db.Column(db.String(140))
    reaction_time = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))

    def __repr__(self):
        return '<Test {}: {}>'.format(self.testname, self.score)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)