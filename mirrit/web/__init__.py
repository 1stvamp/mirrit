# -*- coding: utf-8 -*-
"""Main Flask app for mirrit web UI
"""

from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
# Add twitter-bootstrap goodness
Bootstrap(app)

app.secret_key = 'foobar'
app.config['BOOTSTRAP_USE_MINIFIED'] = True
app.config['BOOTSTRAP_USE_CDN'] = True
app.config['BOOTSTRAP_FONTAWESOME'] = True
app.config['BOOTSTRAP_CUSTOM_CSS'] = True

import mirrit.web.views
