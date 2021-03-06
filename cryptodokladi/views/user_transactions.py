from pyramid.compat import escape
import re
from docutils.core import publish_parts

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
)

from pyramid.view import view_config
from sqlalchemy import func, union, select

from ..models import User, Funds, Token

from ..transactions.transaction import getTransactions, getTokenSums, transaction


@view_config(route_name='user_transactions', renderer='json', permission='view')
def user_transactions(request):
    username = request.matchdict['username']
    user = request.dbsession.query(User).filter_by(name=username).first()
    token = request.dbsession.query(Token)

    transactions = []
    for t in token:
        for row in getTransactions(request, user, t.token).order_by(Funds.timestamp.desc()):
            transactions.append({
                'token': row.token,
                'value': float(row.value),
                'timestamp': str(row.timestamp),
                'comment': row.comment,
                'user': row.user.name,
                'sender': row.sender.name if row.sender else ""
            })

    return transactions

@view_config(route_name='user_view', renderer='../templates/user_view.jinja2', permission='view')
def user_view(request):
    user = request.context.user
    token = request.dbsession.query(Token)

    # Get sums from all transactions by currencies
    tokens = getTokenSums(request, user)

    # Get all transactions for each currency.
    transactions = []

    for t in token:
        transactions.append({
            'token': t.name,
            'transactions': getTransactions(request, user, t.token)
        })

    funds_add = request.route_url('add_funds', username=user.name)
    funds_send = request.route_url('send_funds', username=user.name)
    return dict(
        user=user,
        tokens=tokens,
        transactions=transactions,
        add_funds=funds_add,
        send_funds=funds_send
    )

@view_config(route_name='user_list', renderer='../templates/user_list.jinja2', permission='list')
def user_list(request):
    users = request.dbsession.query(User).all()
    token = request.dbsession.query(Token)

    user_funds = []
    for u in users:
        user = {
            'name': u.name,
            'BTC': 0,
            'ETH': 0,
            'SPF': 0,
            'PIVX': 0,
            'XMR': 0,
            'DTR': 0
        }

        for tokens in getTokenSums(request, u).all():
            user[tokens.token] = tokens.value

        user_funds.append(user)

    return dict(user_funds=user_funds, token=token)


@view_config(route_name='add_multiple_funds', renderer='../templates/user_add_multiple_funds.jinja2', permission='call')
def add_multiple_funds(request):
    users = request.dbsession.query(User.name)
    token = request.dbsession.query(Token)
    
    return dict(users=users, token=token)

@view_config(route_name='add_multiple_funds_call', renderer='json', permission='call')
def add_multiple_funds_call(request):
    successful_transactions = []

    try:
        rate = float(request.matchdict['rate'])
        sending_user = request.user
        token = request.matchdict['token']

        successful_transactions.append({
            'sending_user': sending_user,
            'token': token,
            'rate': rate
        })

        for el in request.json_body:
            try:
                value = float(el[1])
                if (value == 0):
                    continue

                # Value is set by rate set by the editor
                value = value / rate
                receiving_user = request.dbsession.query(User).filter_by(name=el[0]).first()
                comment = el[2]

                if (receiving_user != None):
                    transaction(request, token, value, comment, sending_user, receiving_user)
                    successful_transactions.append({
                        'receiving_user': receiving_user.name,
                        'value': value,
                        'comment': comment
                    })
            except ValueError:
                continue
    finally:
        print(successful_transactions)
        return HTTPFound(location=request.route_url('view_page', pagename='FrontPage'))


@view_config(route_name='add_funds', renderer='../templates/user_add_funds.jinja2', permission='create')
def add_funds(request):
    user = request.context.user
    token = request.dbsession.query(Token)
    
    # Get sums from all transactions by currencies
    tokens = getTokenSums(request, user)
    
    if 'form.submitted' in request.params:
        token = request.params['token']
        value = request.params['value']
        comment = request.params['comment']

        fund = Funds(token=token, value=value, comment=comment, user=user)
        request.dbsession.add(fund)

        next_url = request.route_url('user_view', username=user.name)
        return HTTPFound(location=next_url)
    
    return dict(user=user, tokens=tokens, token=token)

@view_config(route_name='send_funds', renderer='../templates/user_send_funds.jinja2', permission='send')
def send_funds(request):
    sending_user = request.user
    token = request.dbsession.query(Token)
    
    # Get sums from all transactions by currencies
    tokens = getTokenSums(request, sending_user)

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

        transaction(request, token, value, comment, sending_user, receiving_user)

        next_url = request.route_url('user_view', username=sending_user.name)
        return HTTPFound(location=next_url)

    return dict(user=sending_user, tokens=tokens, users=users, token=token)
