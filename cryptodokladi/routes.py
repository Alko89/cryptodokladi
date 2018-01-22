from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound,
)
from pyramid.security import (
    Allow,
    Everyone,
)

from .models import Page, User

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('view_wiki', '/')
    config.add_route('solidity', '/solidity')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('songs_list', 'song')
    config.add_route('tag', '/song/tag/{tagname}')
    config.add_route('song_add', '/song/add')
    config.add_route('song_edit', '/song/{songtitle}/edit')
    config.add_route('song', '/song/{songtitle}')

    config.add_route('view_page', '/{pagename}', factory=page_factory)
    config.add_route('add_page', '/add_page/{pagename}', factory=new_page_factory)
    config.add_route('edit_page', '/{pagename}/edit_page', factory=page_factory)

    config.add_route('user_list', '/user/user_list', factory=user_list_factory)
    config.add_route('user_new', '/user/user_new', factory=user_list_factory)
    config.add_route('user_settings', '/user/settings/{username}', factory=user_change_settings)
    config.add_route('user_settings_save', '/user/settings/{username}/save', factory=user_change_settings)
    config.add_route('user_view', '/user/{username}', factory=user_factory)
    config.add_route('add_funds', '/user/add_funds/{username}', factory=add_funds_factory)
    config.add_route('send_funds', '/user/send_funds/{username}', factory=send_funds_factory)


def new_page_factory(request):
    pagename = request.matchdict['pagename']
    if request.dbsession.query(Page).filter_by(name=pagename).count() > 0:
        next_url = request.route_url('edit_page', pagename=pagename)
        raise HTTPFound(location=next_url)
    return NewPage(pagename)

class NewPage(object):
    def __init__(self, pagename):
        self.pagename = pagename

    def __acl__(self):
        return [
            (Allow, 'role:editor', 'create'),
            (Allow, 'role:basic', 'create'),
        ]

def page_factory(request):
    pagename = request.matchdict['pagename']
    page = request.dbsession.query(Page).filter_by(name=pagename).first()
    if page is None:
        raise HTTPNotFound
    return PageResource(page)

class PageResource(object):
    def __init__(self, page):
        self.page = page

    def __acl__(self):
        return [
            (Allow, Everyone, 'view'),
            (Allow, 'role:editor', 'edit'),
            (Allow, str(self.page.creator_id), 'edit'),
        ]




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
