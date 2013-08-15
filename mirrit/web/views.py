# -*- coding: utf-8 -*-
"""Flask app views for mirrit web UI
"""

import os
from flask.json import loads
from flaskext.github import GithubAuth
from flaskext import simpleregistration
from flask import g, request, url_for, render_template, redirect

from mirrit.web import app
from mirrit.web.models import User
from mirrit.web.forms import LoginForm, SignupForm

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


@app.context_processor
def add_user_dict_to_template():
    user = g.user.for_json() if g.user else {}
    return {'user': user}


@app.route('/')
def home():
    context = {}
    if token_getter():
        resp, repos = github.get_resource('user/repos')
        context['github_repos'] = loads(repos)
    return render_template('index.html', **context)


@app.route('/oauth/github/login')
def github_auth():
    if not g.user.github_access_token:
        return github.authorize(callback_url=url_for('github_callback',
                                                     _external=True))
    else:
        return redirect(url_for('home'))


@app.route('/oauth/github/callback')
@github.authorized_handler
def github_callback(resp):
    next_url = request.args.get('next') or url_for('home')

    if resp is not None and g.user is not None:
        g.user.github_access_token = resp['access_token']
        g.user.persist()

    return redirect(next_url)
