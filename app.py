from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
app.debug = True
app.config['DEBUG'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

@app.route("/",  methods=('GET', 'POST'))
def index():
	tasks = Task.query.all()
	form = MyForm()
	if form.validate_on_submit():
		task = Task(body=form.body.data)
		db.session.add(task)
		db.session.commit()
		return redirect(request.referrer or url_for('index'))
	return render_template('index.html', tasks=tasks, form=form)

class MyForm(FlaskForm):
	body = StringField('New Task', validators=[DataRequired()])
	submit = SubmitField(('Submit'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(request.referrer or url_for('index'))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Task {}>'.format(self.body)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Task': Task}