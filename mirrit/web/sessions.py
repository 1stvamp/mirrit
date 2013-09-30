from flask.ext.pymongo import PyMongo
from flask.sessions import SessionMixin
from werkzeug.datastructures import CallbackDict
from flask.ext.mongo_sessions import MongoDBSessionInterface

from mirrit.web import app


class MongoDBSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None, new=True):
        def on_update(this):
            this.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False

    def pack(self):
        return dict(self)


mongo = PyMongo(app)
with app.app_context():
    # Override the session class so we can just store a BSON object, rather
    # than packing
    MongoDBSessionInterface.session_class = MongoDBSession
    app.session_interface = MongoDBSessionInterface(app, mongo.db, 'sessions')
