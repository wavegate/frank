from flask_wtf import FlaskForm
from wtforms import BooleanField, DateTimeField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, ValidationError, Length
from wtforms.fields import DateField
from app.models import User

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

