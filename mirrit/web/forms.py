from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email

from .models import User


class LoginForm(Form):
    user = None

    username = TextField('username', validators=(DataRequired(),))
    password = PasswordField('password', validators=(DataRequired(),))

    def validate(self):
        user = User.get_by_login(self.username, self.password)

        if user:
            self.user = user
            return True
        else:
            return False


class SignupForm(Form):
    username = TextField('username', validators=(DataRequired(),))
    password = PasswordField('password', validators=(DataRequired(),))
    email = TextField('email', validators=(Email(), DataRequired()))

    def save(self):
        return {}
