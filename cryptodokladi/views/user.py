from pyramid.compat import escape
import re
from docutils.core import publish_parts

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
)

from pyramid.view import view_config
from sqlalchemy import func, union, select

from ..models import User, Funds

def getTransactions(request, user, token):
    transactions_btc_r = request.dbsession.query(Funds).filter_by(user=user).filter(Funds.token==token)
    transactions_btc_s = request.dbsession.query(Funds).filter_by(sender=user).filter(Funds.token==token)
    return transactions_btc_r.union(transactions_btc_s).order_by(Funds.timestamp.desc())

def getTokenSums(request, user):
    tokens_r = request.dbsession.query(Funds.token.label('token'), func.sum(Funds.value).label('value')).filter_by(user=user).group_by(Funds.token)
    tokens_s = request.dbsession.query(Funds.token.label('token'), -func.sum(Funds.value).label('value')).filter_by(sender=user).group_by(Funds.token)
    tokens_u = union(tokens_r, tokens_s).alias('funds')
    return request.dbsession.query(tokens_u.columns.token, func.sum(tokens_u.columns.value).label('value')).group_by(Funds.token)

@view_config(route_name='user_transactions', renderer='json', permission='view')
def user_transactions(request):
    user = request.context.user

    transactions = []
    for row in getTransactions(request, user, 'BTC'):
        transactions.append({
            'token': row.token,
            'value': float(row.value),
            'timestamp': str(row.timestamp),
            'comment': row.comment,
            'sender': row.sender.name if row.sender else ""
        })
    for row in getTransactions(request, user, 'ETH'):
        transactions.append({
            'token': row.token,
            'value': float(row.value),
            'timestamp': str(row.timestamp),
            'comment': row.comment,
            'sender': row.sender.name if row.sender else ""
        })
    for row in getTransactions(request, user, 'SPF'):
        transactions.append({
            'token': row.token,
            'value': float(row.value),
            'timestamp': str(row.timestamp),
            'comment': row.comment,
            'sender': row.sender.name if row.sender else ""
        })
    for row in getTransactions(request, user, 'PIVX'):
        transactions.append({
            'token': row.token,
            'value': float(row.value),
            'timestamp': str(row.timestamp),
            'comment': row.comment,
            'sender': row.sender.name if row.sender else ""
        })

    return transactions

@view_config(route_name='user_view', renderer='../templates/user_view.jinja2', permission='view')
def user_view(request):
    user = request.context.user

    # Get sums from all transactions by currencies
    tokens = getTokenSums(request, user)

    # Get all transactions for each currency.
    transactions_btc = getTransactions(request, user, 'BTC')
    transactions_eth = getTransactions(request, user, 'ETH')
    transactions_pivx= getTransactions(request, user, 'PIVX')
    transactions_spf = getTransactions(request, user, 'SPF')

    funds_add = request.route_url('add_funds', username=user.name)
    funds_send = request.route_url('send_funds', username=user.name)
    return dict(
        user=user,
        tokens=tokens,
        transactions_btc=transactions_btc,
        transactions_eth=transactions_eth,
        transactions_pivx=transactions_pivx,
        transactions_spf=transactions_spf,
        add_funds=funds_add,
        send_funds=funds_send
    )

@view_config(route_name='user_list', renderer='../templates/user_list.jinja2', permission='list')
def user_list(request):
    users = request.dbsession.query(User).all()

    user_funds = []
    sums = [0, 0, 0, 0]
    for u in users:
        user = {
            'name': u.name,
            'BTC': 0,
            'ETH': 0,
            'PIVX': 0,
            'SPF': 0
        }

        for token in getTokenSums(request, u).all():
            user[token.token] = token.value

        sums[0] = sums[0] + user['BTC']
        sums[1] = sums[1] + user['ETH']
        sums[2] = sums[2] + user['SPF']
        sums[3] = sums[3] + user['PIVX']

        user_funds.append(user)

    return dict(user_funds=user_funds, sums=sums)


@view_config(route_name='add_multiple_funds', renderer='../templates/user_add_multiple_funds.jinja2', permission='call')
def add_multiple_funds(request):
    users = request.dbsession.query(User.name)
    
    return dict(users=users)

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

        transaction(request, token, value, comment, sending_user, receiving_user)

        next_url = request.route_url('user_view', username=sending_user.name)
        return HTTPFound(location=next_url)

    return dict(user=sending_user, tokens=tokens, users=users)

def transaction(request, token, value, comment, sending_user, receiving_user):
    # fund_send = Funds(token=token, value=-value, comment=comment, user=sending_user)
    fund_receive = Funds(token=token, value=value, comment=comment, user=receiving_user, sender=sending_user)

    # request.dbsession.add(fund_send)
    request.dbsession.add(fund_receive)


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
