import requests
import simplejson as json
from flask import Flask, request
from flaskext import simpleregistration

from .models import User
from .forms import LoginForm, SignupForm

from gevent.monkey import patch_all
patch_all()

app = Flask('mirrit')

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


@app.route('/')
def home():
    return 'OK', 200

if __name__ == '__main__':
    # Probably never used, run with the runserver entrypoint instead
    app.run(debug=True)
