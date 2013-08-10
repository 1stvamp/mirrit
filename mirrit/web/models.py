from humbledb import Mongo, Document


class User(Document):
    username = ''
    password = ''
    email = ''

    @property
    def id(self):
        return unicode(self._id)

    def save(self):
        with Mongo:
            super(User, self).save(self, w=1)
