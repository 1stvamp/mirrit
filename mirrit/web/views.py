# -*- coding: utf-8 -*-
"""Flask app views for mirrit web UI
"""

import os
from hashlib import sha1
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
    if g.user and 'tracked_repos' not in session:
        session['tracked_repos'] = []
        for repo in TrackedRepo.query.filter_by(user_id=g.user.id).all():
            session['tracked_repos'].append(repo.path)

    if 'github_repos' in session:
        context['github_repos'] = session['github_repos']
    elif token_getter():
        _, full_repos = github.get_resource('user/repos')
        repos = {}
        for repo in loads(full_repos):
            repos[sha1(repo['url']).hexdigest()] = {
                'full_name': repo['full_name'],
                'git_url': repo['git_url'],
                'private': repo['private'],
                'url': repo['url'],
                'is_tracked': repo['url'] in session['tracked_repos']
            }
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
    path = request.args.get('path')
    repo = TrackedRepo.query.filter_by(path=path).first()

    if not repo:
        repo = TrackedRepo(path, g.user)
        db.session.add(repo)
        db.session.commit()

    tracked_repos = session.get('tracked_repos', [])
    if path not in tracked_repos:
        tracked_repos.append(path)

    session['github_repos'][sha1(path).hexdigest()]['is_tracked'] = True

    return url_for('home')


@app.route('/repos/', methods=('DELETE',))
@login_required
def delete_repo():
    path = request.args.get('path')

    db.session.query(TrackedRepo).filter(
            TrackedRepo.path == path,
            TrackedRepo.user_id == g.user.id).delete()

    tracked_repos = session.get('tracked_repos', [])
    if path in tracked_repos:
        tracked_repos.remove(path)

    session['github_repos'][sha1(path).hexdigest()]['is_tracked'] = False

    return url_for('home')
