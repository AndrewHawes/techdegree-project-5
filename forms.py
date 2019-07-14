import datetime

from flask_wtf import FlaskForm
from wtforms import (DateField, IntegerField, PasswordField, StringField,
                     TextAreaField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length, Regexp,
                                ValidationError)

from models import User


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class EntryForm(FlaskForm):
    title = StringField(validators=[DataRequired("A title is required.")])
    date = DateField(validators=[DataRequired()], default=datetime.date.today)
    time = IntegerField(
        validators=[
            DataRequired("Time spent must be an integer greater than zero.")
        ])
    learned = TextAreaField()
    resources = TextAreaField()
    tags = StringField()


class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired("Username is required."),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message="Username can only contain alphanumeric characters "
                        "and underscores."
            ),
            name_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired("Email is required."),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired("Password is required."),
            Length(min=2),
            EqualTo('password2', message="Passwords do not match.")
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired("Password confirmation is required.")]
    )


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
