from sys import exit
from gevent.wsgi import WSGIServer
from gevent.monkey import patch_all

from mirrit.web import app

# Patch socket calls to go via Gevent
patch_all()


def main():
    app.debug = True
    WSGIServer(('', 5000), app).serve_forever()
    return 0

if __name__ == '__main__':
    exit(main())
