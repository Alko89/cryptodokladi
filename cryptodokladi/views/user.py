from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
)

from pyramid.view import view_config
from sqlalchemy import func, union, select

from ..models import User


@view_config(route_name='user_new', renderer='../templates/user_new.jinja2', permission='new')
def user_new(request):
    if 'form.submitted' in request.params:
        name = request.params['name']
        password = request.params['password']

        user = User(name=name, role='basic')
        user.set_password(password)
        request.dbsession.add(user)

        next_url = request.route_url('user_view', username=user.name)
        return HTTPFound(location=next_url)
    save_url = request.route_url('user_new')
    return dict(save_url=save_url)

@view_config(route_name='user_settings', renderer='../templates/user_settings.jinja2', permission='save')
def user_settings(request):
    username = request.matchdict['username']
    user = request.dbsession.query(User).filter_by(name=username).first()

    if 'form.submitted' in request.params:
        password = request.params['password']
        repassword = request.params['repassword']

        if password != repassword:
            return HTTPFound(location=request.route_url('user_settings_save', username=user.name))

        user.set_password(password)
        return HTTPFound(location=request.route_url('view_page', pagename='FrontPage'))

    return dict(user=user)
