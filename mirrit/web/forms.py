from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email

from mirrit.web.models import db, User


class LoginForm(Form):
    user = None

    username = TextField('username', validators=(DataRequired(),))
    password = PasswordField('password', validators=(DataRequired(),))

    SECRET_KEY = 'foobar'

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        user = User.query.filter_by(username=self.data['username']).first()

        if user and user.verify_password(self.data['password']):
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
            user = User(**self.data)
            db.session.add(user)
            db.session.commit()
            return user
