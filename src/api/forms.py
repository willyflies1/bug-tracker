"""Signup & login forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from src.api.bug import Bug


class ChooseProject(FlaskForm, user_name):
    """User chooses from their own projects."""
    bugs = Bug.get_bugs_by_user(user_name=user_name)

    projectsField = SelectField


    name = StringField('Name',
                       validators=[DataRequired()])
    email = StringField('Email',
                        validators=[Length(min=6),
                                    Email(message='Enter a valid email.'),
                                    DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password',
                            validators=[DataRequired(),
                                        EqualTo('password', message='Passwords must match.')])
    website = StringField('Website',
                          validators=[Optional()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Login Form."""
    email = StringField('Email', validators=[DataRequired(),
                                             Email(message='Enter a valid email.')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')