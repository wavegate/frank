from flask import flash, Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, LoginManager, login_required, login_user, logout_user, UserMixin
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_moment import Moment
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from wtforms import BooleanField, DateTimeField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, ValidationError
#from wtforms.fields.html5 import DateField
from wtforms.fields import DateField

import os
from datetime import datetime
import sys #just for console printing, can remove after

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
app.debug = True
app.config['DEBUG'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
csrf = CSRFProtect(app)
moment = Moment(app)
login.login_view = 'login'

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/")
def index():
	return redirect(url_for('tasks'))

@app.route("/tasks", methods=['GET', 'POST'])
@login_required
def tasks():
	tasks = current_user.tasks.order_by(Task.last_updated.desc()).all()
	form = TaskForm()
	return render_template('tasks.html', tasks=tasks, form=form)

@app.route("/create_task", methods=['POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, notes = form.notes.data, deadline=form.deadline.data, start_time=form.start_time.data, end_time=form.end_time.data, author=current_user)
        db.session.add(task)
        db.session.commit()
    return redirect(request.referrer or url_for('tasks'))

@app.route("/fitness", methods=['GET'])
@login_required
def fitness():
    return render_template('fitness.html')

@app.route("/schedule", methods=['GET'])
@login_required
def schedule():
    tasks = current_user.tasks.order_by(Task.start_time.desc()).all()
    return render_template('schedule.html', tasks=tasks)

@app.route("/profile", methods=['GET'])
@login_required
def profile():
    return render_template('profile.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(request.referrer or url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    #email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    deadline = DateTimeField('Deadline', format="%m/%d/%Y %I:%M %p", validators=[Optional()])
    start_time = DateTimeField('Start Time', format="%m/%d/%Y %I:%M %p", validators=[Optional()])
    end_time = DateTimeField('End Time', format="%m/%d/%Y %I:%M %p", validators=[Optional()])
    submit = SubmitField('Submit')

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if current_user == task.author:
        db.session.delete(task)
        db.session.commit()
    return redirect(request.referrer or url_for('index'))

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    form = TaskForm()
    if form.validate_on_submit() and current_user == task.author:
        task.title=form.title.data
        task.notes=form.notes.data
        task.deadline=form.deadline.data
        task.start_time=form.start_time.data
        task.end_time=form.end_time.data
        task.last_updated=datetime.now()
        db.session.commit()
        return redirect(url_for('tasks'))
    return render_template('edit_task.html', task=task, form=form)

@app.route('/change_task_completion/<int:task_id>')
def change_task_completion(task_id):
    task = Task.query.get(task_id)
    if current_user == task.author:
        if task.complete:
        	task.complete = False
        else:
        	task.complete = True
        task.last_updated = datetime.now()
        db.session.commit()
    return redirect(request.referrer or url_for('index'))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='author', lazy='dynamic')
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
    isEvent = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Task {}>'.format(self.title)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Task': Task, 'User': User}