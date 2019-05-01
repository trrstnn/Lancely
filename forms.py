from flask_wtf import FlaskForm as Form

from wtforms import HiddenField, TextField, TextAreaField, SubmitField, StringField, PasswordField, IntegerField, BooleanField
from wtforms import SelectField

from wtforms.validators import (DataRequired, Regexp, ValidationError, Email, Length, EqualTo, NumberRange)

from flask_login import UserMixin

from flask_bcrypt import generate_password_hash

from models import User

def name_exists(form, field):
    if User.select().where(User.username == field.data). exists():
        raise ValidationError("User with this username already exists!")

def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("Someone with this email is already in the DB")





class RegisterForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, numbers, and underscores only")
            ),
            name_exists
        ])
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators = [
            DataRequired(),
            Length(min=2),
            EqualTo('Password2', message='Passwords must match')
        ])
    Password2 = PasswordField(
        'Confirm Password',
        validators = [DataRequired()]
    )
    name = StringField(
        'Name',
        validators = [
            DataRequired()
        ])
    freelancer = BooleanField(
        'Are you a freelancer?'
        )
    location = StringField(
        'Where are you located?',
        validators = [
            DataRequired()
        ])
    lng = HiddenField(
    
        validators = [
            DataRequired()
        ])
    lat = HiddenField(
       
        validators = [
            DataRequired()
        ])
  
class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators=[DataRequired() ])


class UpdateUserForm(Form):
    # username = TextField("Username")
    # email = TextField("Email")
    # name = TextField("Name")
    summary = TextAreaField("Tell me more about yourself?")
    category = SelectField('Work type:',
        choices=[('planner', 'Event Planner'), ('bartender', 'Bartender'), ('photographer', 'Photographer'),('videographer', 'Videographer'),('dj', 'DJ'),('audio','Audio Engineer')]
    )
    experience = IntegerField("How many years have you been doing this?")
    skills = TextAreaField("Skills")
    rate = IntegerField("What is your hourly rate?")
    location = TextAreaField("New Address")
    submit = SubmitField('Edit Profile')

class ReviewForm(Form):
  title = TextField("By:")
  rating = IntegerField("rate 1-5")
  content = TextAreaField("Content") 
  submit = SubmitField('Submit Comment')
