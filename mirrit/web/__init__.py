from flask import Flask

app = Flask('mirrit.web')
app.secret_key = 'foobar'
