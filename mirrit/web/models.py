from humbledb import Mongo, Document


class User(Document):
    username = ''
    password = ''
    email = ''

    @property
    def id(self):
        return unicode(self._id)

    @property
    def user_id(self):
        return unicode(self._id)

    @staticmethod
    def get_by_login(cls, username, password):
        with Mongo:
            return cls.find({'username': username,
                             'password': password})

    def save(self):
        with Mongo:
            super(User, self).save(self, w=1)
