from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound,
)
from pyramid.security import (
    Allow,
    Everyone,
)

from .models import User

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('login', '/')
    config.add_route('logout', '/logout')

    config.add_route('user_list', '/user/user_list', factory=user_list_factory)
    config.add_route('user_new', '/user/user_new', factory=user_list_factory)
    config.add_route('user_settings', '/user/settings/{username}', factory=user_change_settings)
    config.add_route('user_settings_save', '/user/settings/{username}/save', factory=user_change_settings)
    config.add_route('user_view', '/user/{username}', factory=user_factory)
    config.add_route('add_funds', '/user/add_funds/{username}', factory=add_funds_factory)
    config.add_route('send_funds', '/user/send_funds/{username}', factory=send_funds_factory)



def user_factory(request):
    username = request.matchdict['username']
    user = request.dbsession.query(User).filter_by(name=username).first()
    if User is None:
        raise HTTPNotFound
    return UserResource(user)

class UserResource(object):
    def __init__(self, user):
        self.user = user

    def __acl__(self):
        return [
            (Allow, str(self.user.id), 'view'),
            (Allow, 'role:editor', 'view'),
        ]

def user_list_factory(request):
    return UserList()

class UserList(object):
    def __acl__(self):
        return [
            (Allow, 'role:editor', 'list'),
            (Allow, 'role:editor', 'new')
        ]

def add_funds_factory(request):
    username = request.matchdict['username']
    user = request.dbsession.query(User).filter_by(name=username).first()
    if user is None:
        raise HTTPNotFound
    return AddFunds(user)

class AddFunds(object):
    def __init__(self, user):
        self.user = user

    def __acl__(self):
        return [
            (Allow, 'role:editor', 'create')
        ]

def send_funds_factory(request):
    user = request.user
    if user is None:
        raise HTTPNotFound
    return SendFunds(user)

class SendFunds(object):
    def __init__(self, user):
        self.user = user

    def __acl__(self):
        return [
            (Allow, str(self.user.id), 'send')
        ]

def user_change_settings(request):
    username = request.matchdict['username']
    user = request.dbsession.query(User).filter_by(name=username).first()
    if user is None:
        raise HTTPNotFound
    return UserChangeSettings(user)

class UserChangeSettings(object):
    def __init__(self, user):
        self.user = user

    def __acl__(self):
        return [
            (Allow, str(self.user.id), 'save'),
            (Allow, 'role:editor', 'save')
        ]
