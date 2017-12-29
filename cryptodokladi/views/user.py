from pyramid.compat import escape
import re
from docutils.core import publish_parts

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
)

from pyramid.view import view_config
from sqlalchemy import func

from ..models import User, Funds


@view_config(route_name='user_view', renderer='../templates/user_view.jinja2', permission='view')
def user_view(request):
    user = request.context.user

    tokens = request.dbsession.query(Funds.token, func.sum(Funds.value).label('value')).filter_by(user=user).group_by(Funds.token)
    funds_add = request.route_url('add_funds', username=user.name)

    return dict(user=user, tokens=tokens, add_funds=funds_add)

@view_config(route_name='user_list', renderer='../templates/user_list.jinja2', permission='list')
def user_list(request):
    user_funds = request.dbsession.query(User.name, Funds.token, func.sum(Funds.value).label('value')).outerjoin(Funds).group_by(User.name).group_by(Funds.token)

    return dict(user_funds=user_funds)

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

@view_config(route_name='add_funds', renderer='../templates/user_edit.jinja2', permission='create')
def add_funds(request):
    edit_user = request.context.user
    
    if 'form.submitted' in request.params:
        token = request.params['token']
        value = float(request.params['value'])
        
        if token == "BTC":
            # Convert value to Satoshi
            value = int(value * 100000000)
        elif token == "ETH":
            # Convert value to Wei
            value = int(value * 1000000000000000000)

        fund = Funds(token=token, value=value, user=edit_user)
        request.dbsession.add(fund)

        next_url = request.route_url('user_view', username=edit_user.name)
        return HTTPFound(location=next_url)
    save_url = request.route_url('add_funds', username=edit_user.name)
    return dict(user=edit_user, save_url=save_url)
