from humbledb import Mongo, Document


class User(Document):
    username = ''
    password = ''
    email = ''
    config_database = 'mirrit'
    config_collection = 'users'

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

    def persist(self):
        with Mongo:
            if self._id:
                super(User, self).__self_class__.update({'_id': self._id}, self, w=1)
            else:
                super(User, self).__self_class__.insert(self, w=1)
