from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    PasswordField,
    DateField,
    IntegerField,
    SelectField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    URL
)

class LoginForm(FlaskForm): #these have csrf validators but I turned them off because I'm doing it manually
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Sign In')
        
class RegistrationForm(FlaskForm):
    first_name = StringField('First')
    last_name = StringField('Last')
    email = StringField('Email')
    password = PasswordField('Password')
    password2 = PasswordField('Repeat Password')
    submit = SubmitField('Register')