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

    transactions_btc = request.dbsession.query(Funds).filter_by(user=user).filter(Funds.token=='BTC').order_by(Funds.timestamp.desc())
    transactions_eth = request.dbsession.query(Funds).filter_by(user=user).filter(Funds.token=='ETH').order_by(Funds.timestamp.desc())
    transactions_pivx = request.dbsession.query(Funds).filter_by(user=user).filter(Funds.token=='PIVX').order_by(Funds.timestamp.desc())
    transactions_spf = request.dbsession.query(Funds).filter_by(user=user).filter(Funds.token=='SPF').order_by(Funds.timestamp.desc())
    transactions_iota = request.dbsession.query(Funds).filter_by(user=user).filter(Funds.token=='IOTA').order_by(Funds.timestamp.desc())

    funds_add = request.route_url('add_funds', username=user.name)
    funds_send = request.route_url('send_funds', username=user.name)
    return dict(
        user=user,
        tokens=tokens,
        transactions_btc=transactions_btc,
        transactions_eth=transactions_eth,
        transactions_pivx=transactions_pivx,
        transactions_spf=transactions_spf,
        transactions_iota=transactions_iota,
        add_funds=funds_add,
        send_funds=funds_send
    )

@view_config(route_name='user_list', renderer='../templates/user_list.jinja2', permission='list')
def user_list(request):
    user_funds = request.dbsession.execute("""
    SELECT users.name,
        SUM(CASE WHEN funds.token = 'BTC' THEN funds.value ELSE 0 END) AS BTC,
        SUM(CASE WHEN funds.token = 'ETH' THEN funds.value ELSE 0 END) AS ETH,
        SUM(CASE WHEN funds.token = 'PIVX' THEN funds.value ELSE 0 END) AS PIVX,
        SUM(CASE WHEN funds.token = 'SPF' THEN funds.value ELSE 0 END) AS SPF,
        SUM(CASE WHEN funds.token = 'IOTA' THEN funds.value ELSE 0 END) AS IOTA
    FROM funds
    INNER JOIN users ON users.id = funds.user_id
    GROUP BY users.name
    """)

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

@view_config(route_name='add_funds', renderer='../templates/user_add_funds.jinja2', permission='create')
def add_funds(request):
    user = request.context.user
    tokens = request.dbsession.query(Funds.token, func.sum(Funds.value).label('value')).filter_by(user=user).group_by(Funds.token)
    
    if 'form.submitted' in request.params:
        token = request.params['token']
        value = request.params['value']
        comment = request.params['comment']

        fund = Funds(token=token, value=value, comment=comment, user=user)
        request.dbsession.add(fund)

        next_url = request.route_url('user_view', username=user.name)
        return HTTPFound(location=next_url)
    
    return dict(user=user, tokens=tokens)

@view_config(route_name='send_funds', renderer='../templates/user_send_funds.jinja2', permission='send')
def send_funds(request):
    sending_user = request.user
    tokens = request.dbsession.query(Funds.token, func.sum(Funds.value).label('value')).filter_by(user=sending_user).group_by(Funds.token)
    users = request.dbsession.query(User.id, User.name).all()
    
    if 'form.submitted' in request.params:
        receiving_userid = request.params['receiving_user']
        receiving_user = request.dbsession.query(User).filter_by(id=receiving_userid).first()
        token = request.params['token']
        value = float(request.params['value'].replace(',', '.'))
        comment = request.params['comment']

        if value < 0:
            back = request.route_url('send_funds', username=sending_user.name)
            return HTTPFound(location=back)

        fund_send = Funds(token=token, value=-value, comment=receiving_user.name + ": " + comment, user=sending_user)
        fund_receive = Funds(token=token, value=value, comment=comment, user=receiving_user, sender=sending_user)

        request.dbsession.add(fund_send)
        request.dbsession.add(fund_receive)

        next_url = request.route_url('user_view', username=sending_user.name)
        return HTTPFound(location=next_url)

    return dict(user=sending_user, tokens=tokens, users=users)


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
