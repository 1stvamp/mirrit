# -*- coding: utf-8 -*-
"""Flask app routes for mirrit web UI
"""

import os
from flask import g, request, url_for, render_template, redirect, Flask
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


@github.access_token_getter
def token_getter():
    if g.user is not None:
        return g.user.github_access_token


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/oauth/github/login')
def auth_github():
    if g.user.github_access_token is '':
        return github.authorize(callback_url=url_for('github_callback'))
    else:
        return url_for('home')


@app.route('/oauth/github/callback')
@github.authorized_handler
def github_callback(resp):
    next_url = request.args.get('next') or url_for('home')

    if resp is not None and g.user is not None:
        g.user.github_access_token = resp['access_token']
        g.user.persist()

    return redirect(next_url)

if __name__ == '__main__':
    # Probably never used, run with the runserver entrypoint instead
    app.run(debug=True)
