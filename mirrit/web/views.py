# -*- coding: utf-8 -*-
"""Flask app views for mirrit web UI
"""

import os
from flask.json import loads
from flaskext.github import GithubAuth
from flask import g, session, request, url_for, render_template, redirect
from flaskext.simpleregistration import SimpleRegistration, login_required

from mirrit.web import app
from mirrit.web.models import db, User, TrackedRepo
from mirrit.web.forms import LoginForm, SignupForm

simplereg = SimpleRegistration(
    app=app,
    user_model=User,
    login_url="/login/",
    login_form=LoginForm,
    login_redirect="home",
    logout_url="/logout/",
    logout_redirect="home",
    signup_url="/signup/",
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
    context = {}
    if 'github_repos' in session:
        context['github_repos'] = session['github_repos']
    elif token_getter():
        _, full_repos = github.get_resource('user/repos')
        repos = []
        for repo in loads(full_repos):
            repos.append({
                'full_name': repo['full_name'],
                'git_url': repo['git_url'],
                'private': repo['private']
            })
        session['github_repos'] = context['github_repos'] = repos
    return render_template('index.html', **context)


@app.route('/oauth/github/login/')
@login_required
def github_auth():
    if not g.user.github_access_token:
        return github.authorize(callback_url=url_for('github_callback',
                                                     _external=True))
    else:
        return redirect(url_for('home'))


@app.route('/oauth/github/callback/')
@login_required
@github.authorized_handler
def github_callback(resp):
    next_url = request.args.get('next') or url_for('home')

    if resp is not None and g.user is not None:
        g.user.github_access_token = resp['access_token']
        db.session.add(g.user)
        db.session.commit()

    return redirect(next_url)


@app.route('/repos/', methods=('PUT', 'POST'))
@login_required
def add_repo():
    repo = TrackedRepo.query.filter_by(path=request.form['path']).first()

    if not repo:
        repo = TrackedRepo(request.form['path'], g.user)
        db.session.add(repo)
        db.session.commit()

    return url_for('home')


@app.route('/repos/', methods=('DELETE',))
@login_required
def delete_repo():
    db.session.query(TrackedRepo).filter(
            TrackedRepo.path == request.args.get('path'),
            TrackedRepo.user_id == g.user.id).delete()

    return url_for('home')
