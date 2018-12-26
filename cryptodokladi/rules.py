from pyramid.httpexceptions import (
    HTTPUnauthorized,
    HTTPNotFound,
    HTTPFound,
)
from pyramid.security import (
    Allow,
    Everyone,
)

from .models import Page, User


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
        raise HTTPUnauthorized
    return UserResource(user)

def user_id_factory(request):
    id = request.matchdict['id']
    user = request.dbsession.query(User).filter_by(id=id).first()
    if User is None:
        raise HTTPUnauthorized
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
            (Allow, str(self.user.id), 'send'),
            (Allow, 'role:editor', 'view'),
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

def calculate_staking_rewards(request):
    user = request.user
    if user is None:
        raise HTTPNotFound
    return CalculateStakingRewards(user)

class CalculateStakingRewards(object):
    def __init__(self, user):
        self.user = user

    def __acl__(self):
        return [
            (Allow, 'role:editor', 'call'),
            (Allow, 'name:alko', 'calc')
        ]
