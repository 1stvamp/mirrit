from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.bcrypt import Bcrypt

from mirrit.web import app

if 'SQLALCHEMY_DATABASE_URI' not in app.config:
    from os import path
    sl_path = path.join(path.dirname(__file__), 'mirrit.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = sl_path

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, index=True)
    email = db.Column(db.String(256), unique=True, index=True)
    _password = db.Column(db.String(256), index=True)
    github_access_token = db.Column(db.String(128))

    def _set_password(self, password):
        self._password = bcrypt.generate_password_hash(password)

    def _get_password(self):
        return self._password

    password = db.synonym('_password', descriptor=property(_get_password,
                                                           _set_password))

    def __init__(self, username, email, password,
                 github_access_token=None):
        self.username = username
        self.email = email
        self.password = password
        self.github_access_token = github_access_token

    def __repr__(self):
        return u'User("%s", "%s", "...")' % (self.username, self.email)

    @property
    def user_id(self):
        return self.id

    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password, password)
