from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField
from wtforms.validators import DataRequired
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
bootstrap = Bootstrap(app)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/tasks", methods = ('GET', 'POST'))
def tasks():
	tasks = Task.query.all()
	form = MyForm()
	if form.validate_on_submit():
		task = Task(body=form.body.data, deadline=form.deadline.data)
		db.session.add(task)
		db.session.commit()
		return redirect(request.referrer or url_for('tasks'))
	return render_template('tasks.html', tasks=tasks, form=form)

class MyForm(FlaskForm):
	body = StringField('New Task', validators=[DataRequired()])
	deadline = StringField('Deadline')
	submit = SubmitField(('Submit'))

class TaskForm(FlaskForm):
	complete = BooleanField('Complete')

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(request.referrer or url_for('index'))

@app.route('/change_task_completion/<int:task_id>')
def change_task_completion(task_id):
    task = Task.query.get(task_id)
    if task.complete:
    	task.complete = False
    else:
    	task.complete = True
    task.last_updated = datetime.now()
    db.session.commit()
    return redirect(request.referrer or url_for('index'))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    complete = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime, default=datetime.now)
    deadline = db.Column(db.String(140))

    def __repr__(self):
        return '<Task {}>'.format(self.body)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Task': Task}