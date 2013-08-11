import os
from flask import Flask
from flask.json import loads
from flaskext import simpleregistration
from flaskext.github import GithubAuth

from mirrit.web.models import User
from mirrit.web.forms import LoginForm, SignupForm

from gevent.monkey import patch_all
patch_all()

app = Flask('mirrit')
app.secret_key = 'foobar'

simplereg = simpleregistration.SimpleRegistration(
    app=app,
    user_model=User,
    login_url="/login",
    login_form=LoginForm,
    login_redirect="home",
    logout_url="/logout",
    logout_redirect="home",
    signup_url="/signup",
    signup_form=SignupForm,
    signup_redirect="home"
)

# setup flask-github
with open(os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(__file__))), 'config.json'), 'r') as f:

    config_data = f.read()

config = loads(config_data)
github = GithubAuth(
    client_id=config['client_id'],
    client_secret=config['client_secret'],
    session_key='user_id'
)


@app.route('/')
def home():
    return 'OK', 200


@app.route('/oauth/callback')
@github.authorized_handler
def authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        return redirect(next_url)

    token = resp['access_token']
    user = User.query.filter_by(github_access_token=token).first()
    if user is None:
        user = User(token)
        db_session.add(user)
    user.github_access_token = token
    db_session.commit()

    session['user_id'] = user.id

    return 'Success'

if __name__ == '__main__':
    # Probably never used, run with the runserver entrypoint instead
    app.run(debug=True)
