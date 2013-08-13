from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email

from mirrit.web.models import User


class LoginForm(Form):
    user = None

    username = TextField('username', validators=(DataRequired(),))
    password = PasswordField('password', validators=(DataRequired(),))

    SECRET_KEY = 'foobar'

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        user = User.get_by_login(self.data['username'], self.data['password'])

        if user:
            self.user = user
            return True
        else:
            return False


class SignupForm(Form):
    username = TextField('username', validators=(DataRequired(),))
    password = PasswordField('password', validators=(DataRequired(),))
    email = TextField('email', validators=(Email(), DataRequired()))

    SECRET_KEY = 'foobar'

    def save(self):
        if self.validate():
            user = User(self.data)
            user.persist()
            return user
