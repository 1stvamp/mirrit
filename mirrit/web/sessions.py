from flask.sessions import SessionMixin
from werkzeug.datastructures import CallbackDict


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
