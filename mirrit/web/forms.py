from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email


class LoginForm(Form):
    username = TextField('username', validators=(DataRequired(),))
    password = PasswordField('password', validators=(DataRequired(),))


class SignupForm(Form):
    username = TextField('username', validators=(DataRequired(),))
    password = PasswordField('password', validators=(DataRequired(),))
    email = TextField('email', validators=(Email(), DataRequired()))
