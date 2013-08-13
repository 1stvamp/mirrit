from bson.objectid import ObjectId
from humbledb import Mongo, Document


class ClassProperty (property):
    """Subclass property to make classmethod properties possible"""
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class User(Document):
    username = 'username'
    password = 'password'
    email = 'email'
    github_access_token = 'ghtoken'
    config_database = 'mirrit'
    config_collection = 'users'

    @property
    def id(self):
        return unicode(self._id)

    @property
    def user_id(self):
        return unicode(self._id)

    @classmethod
    def get_by_login(cls, username, password):
        with Mongo:
            return cls.find_one({cls.username: username,
                                 cls.password: password})

    def persist(self):
        with Mongo:
            User.save(self, safe=True)


class Wrapper(object):
    def get(self, id):
        with Mongo:
            return User.find_one({User._id: ObjectId(id)})

wrapper = Wrapper()
User.query = wrapper
