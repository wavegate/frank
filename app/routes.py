from flask import flash, render_template, redirect, request, url_for
from flask_login import current_user, LoginManager, login_required, login_user, logout_user, UserMixin
from app import app, db, csrf
from app.forms import LoginForm, RegistrationForm, TaskForm, WeightForm
from app.models import User, Task, Weight, Test
from werkzeug.urls import url_parse
from datetime import datetime

import sys #just for console printing, can remove after

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('tasks'))
    else:
        return redirect(url_for('login'))

@app.route("/progress", methods= ['GET'])
def progress():
    return render_template('progress.html')

@app.route("/health", methods = ['GET'])
@login_required
def health():
    weights = current_user.weights.all()
    labels = (weight.timestamp for weight in weights)
    values = (weight.value for weight in weights)
    values = list(values)
    print('Hello world!', file=sys.stderr)
    weightChange = (max(values) if values else 0) - (min(values) if values else 0)

    return render_template('health.html', weights=weights, labels=labels, values=values, weightChange=weightChange)

@app.route("/add_weight", methods=['GET', 'POST'])
@login_required
def add_weight():
    form = WeightForm()
    if form.validate_on_submit():
        weight = Weight(value = form.value.data, author=current_user)
        db.session.add(weight)
        db.session.commit()
        flash('Weight added.')
        return redirect(url_for('health'))
    return render_template('add_weight.html', form=form)

@app.route('/delete_weight/<int:weight_id>')
def delete_weight(weight_id):
    weight = Weight.query.get(weight_id)
    if current_user == weight.author:
        db.session.delete(weight)
        db.session.commit()
        flash('Weight deleted.')
    return redirect(request.referrer or url_for('health'))

@app.route("/cognition", methods = ['GET'])
@login_required
def cognition():
    tests = current_user.tests.order_by(Test.timestamp.desc()).all()
    return render_template('cognition.html', tests=tests)

@app.route("/test1", methods = ['GET'])
@login_required
def test1():
    return render_template('test1.html')

@app.route('/postmethod', methods = ['POST'])
@csrf.exempt
def get_post_javascript_data():
    test_name = request.form['test_name']
    accuracy = request.form['accuracy']
    score = accuracy
    rt = request.form['rt']
    #print(jsdata, file=sys.stderr)
    #with open('somefile.txt', 'a') as the_file:
    #    the_file.write(jsdata)
    #files = glob.glob(os.path.join(app.instance_path, 'static/img/subitizing/*')) #remove subitizing images, must change once more tests added
    #for f in files:
    #    os.remove(f)
    test = Test(testname=test_name, score=score, reaction_time=rt, accuracy=accuracy, author=current_user)
    db.session.add(test)
    db.session.commit()
    return rt

@app.route('/delete_test/<int:test_id>')
@login_required
def delete_test(test_id):
    test = Test.query.get(test_id)
    if test.author == current_user:
        db.session.delete(test)
        db.session.commit()
    return redirect(request.referrer or url_for('cognition'))

@app.route('/tester', methods=['GET', 'POST'])
@csrf.exempt
def tester():
    clicked=None
    if request.method == "POST":
        clicked=request.form['data']
    return render_template('tester.html')

@app.route("/tasks", methods=['GET', 'POST'])
@login_required
def tasks():
    tasks = current_user.tasks.filter_by(stashed=False).order_by(Task.timestamp.desc()).all()
    stashed_tasks = current_user.tasks.filter_by(stashed=True).order_by(Task.timestamp.desc()).all()
    now = datetime.now()
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, notes = form.notes.data, location = form.location.data, deadline=form.deadline.data, start_time=form.start_time.data, end_time=form.end_time.data, author=current_user, last_updated=datetime.utcnow())
        db.session.add(task)
        db.session.commit()
        flash('Task created.')
        return redirect(url_for('tasks'))
    return render_template('tasks.html', now=now, tasks=tasks, stashed_tasks=stashed_tasks, form=form, action="Create")

@app.route("/new_task", methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, notes = form.notes.data, location = form.location.data, deadline=form.deadline.data, start_time=form.start_time.data, end_time=form.end_time.data, author=current_user, last_updated=datetime.utcnow())
        db.session.add(task)
        db.session.commit()
        flash('Task created.')
        return redirect(url_for('tasks'))
    return render_template('new_task.html', form=form)

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    tasks = current_user.tasks.filter_by(stashed=False).order_by(Task.timestamp.desc()).all()
    stashed_tasks = current_user.tasks.filter_by(stashed=True).order_by(Task.timestamp.desc()).all()
    now = datetime.now()
    task = Task.query.get(task_id)
    form = TaskForm()
    if request.method == 'GET':
        if task.notes:
            form.notes.data = task.notes
        if task.title:
            form.title.data = task.title
        if task.location:
            form.location.data = task.location
        if task.deadline:
            form.deadline.data = task.deadline
        if task.start_time:
            form.start_time.data = task.start_time
        if task.end_time:
            form.end_time.data =task.end_time
    if form.validate_on_submit() and current_user == task.author:
        if form.title.data:
            task.title=form.title.data
        if form.notes.data:
            task.notes=form.notes.data
        if form.location.data:
            task.location=form.location.data
        if form.deadline.data:
            task.deadline=form.deadline.data
        if form.start_time.data:
            task.start_time=form.start_time.data
        if form.end_time.data:
            task.end_time=form.end_time.data
        task.last_updated=datetime.utcnow()
        db.session.commit()
        flash('Task updated.')
        return redirect(url_for('tasks'))
    return render_template('edit_task.html', task=task, form=form)

@app.route('/delete_completed_tasks')
def delete_completed_tasks():
    tasks = current_user.tasks.all()
    for task in tasks:
        if task.complete:
            db.session.delete(task)
    db.session.commit()
    flash('All completed tasks have been deleted.')
    return redirect(request.referrer or url_for('tasks'))

@app.route('/delete_all_tasks')
def delete_all_tasks():
    tasks = current_user.tasks.all()
    for task in tasks:
        db.session.delete(task)
    db.session.commit()
    flash('All tasks have been deleted.')
    return redirect(request.referrer or url_for('tasks'))

@app.route('/stash_task/<int:task_id>')
def stash_task(task_id):
    task = Task.query.get(task_id)
    if current_user == task.author:
        if task.stashed == True:
            task.stashed = False
            flash('Task unstashed.')
        elif task.stashed == False:
            task.stashed = True
            flash('Task stashed.')
        db.session.commit()
    return redirect(request.referrer or url_for('tasks'))

@app.route("/fitness", methods=['GET'])
def fitness():
    return render_template('fitness.html')

@app.route("/settings")
def settings():
    return render_template('settings.html')

@app.route("/schedule", methods=['GET'])
@login_required
def schedule():
    tasks = current_user.tasks.order_by(Task.start_time.desc()).all()
    return render_template('schedule.html', tasks=tasks)

@app.route("/profile", methods=['GET'])
@login_required
def profile():
    return render_template('profile.html')

@app.route("/slumusic", methods=['GET'])
def slumusic():
    return render_template('slumusic.html')

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
        flash('Welcome back, {}!'.format(user.username))
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
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if current_user == task.author:
        db.session.delete(task)
        if current_user.current_task_id == task.id:
            current_user.current_task_id = None
        db.session.commit()
        flash('Task deleted.')
    return redirect(request.referrer or url_for('index'))

@app.route('/set_as_current_task/<int:task_id>')
def set_as_current_task(task_id):
    task = Task.query.get(task_id)
    if current_user == task.author:
        current_user.current_task_id = task_id
        db.session.commit()
        flash('Task marked as current.')
    return redirect(request.referrer or url_for('index'))

@app.route('/change_task_completion/<int:task_id>')
def change_task_completion(task_id):
    task = Task.query.get(task_id)
    if current_user == task.author:
        if task.complete:
            task.complete = False
            flash('Task marked as incomplete.')
        else:
            task.complete = True
            flash('Task marked as complete.')
        task.last_updated = datetime.now()
        db.session.commit()
    return redirect(request.referrer or url_for('index'))