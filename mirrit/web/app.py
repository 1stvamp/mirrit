import requests
import simplejson as json
from flask import Flask, request
from gevent.monkey import patch_all

app = Flask('mirrit')
patch_all()


@app.route('/')
def home():
    return 'OK', 200

if __name__ == '__main__':
    # Probably never used, run with the runserver entrypoint instead
    app.run(debug=True)
