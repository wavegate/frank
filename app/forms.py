from flask_wtf import FlaskForm
from wtforms import BooleanField, DateTimeField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, ValidationError, Length
from wtforms.fields import DateField
from app.models import User

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=140)])
    notes = TextAreaField('Notes')
    location = StringField('Location')
    deadline = DateTimeField('Deadline', format="%m/%d/%Y %I:%M %p", validators=[Optional()])
    start_time = DateTimeField('Start Time', format="%m/%d/%Y %I:%M %p", validators=[Optional()])
    end_time = DateTimeField('End Time', format="%m/%d/%Y %I:%M %p", validators=[Optional()])
    submit = SubmitField('Submit')

class WeightForm(FlaskForm):
    value = StringField('Value', validators=[DataRequired()])
    submit = SubmitField('Submit')
