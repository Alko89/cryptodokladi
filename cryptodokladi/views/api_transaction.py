from cornice import Service
from cornice.validators import marshmallow_body_validator

from ..rules import ( user_factory, send_funds_factory )
from ..models import Funds, FundsSchema, Token, TokenSchema
from ..transactions.transaction import getTransactions, getTokenFunds

import json
import urllib.request
from xml.dom import minidom

funds_schema = FundsSchema(many=True)
token_schema = TokenSchema(many=True)

transactions = Service(name='transactions', path='/api/transactions/{username}/{token}', factory=user_factory)

@transactions.get(permission="view")
def get_transactions(request):
    user = request.context.user
    token = request.matchdict['token']

    t = []
    for row in getTransactions(request, user, token).order_by(Funds.timestamp):
        t.append({
            'token': row.token,
            'value': float(row.value),
            'timestamp': str(row.timestamp),
            'comment': row.comment,
            'user': row.user.name,
            'sender': row.sender.name if row.sender else ""
        })
    return t
    # return funds_schema.dump(getTransactions(request, user, token)).data

tokens = Service(name='tokens', path='/api/tokens')

@tokens.get()
def get_tokens(request):
    tokens = request.dbsession.query(Token)
    return token_schema.dump(tokens).data


ticker = Service(name='ticker', path='/api/ticker/{token}')

@ticker.get()
def get_ticker(request):
    token = request.matchdict['token']
    response = urllib.request.urlopen("https://api.coinmarketcap.com/v1/ticker/" + token + "/?convert=EUR")
    return json.load(response)


rate = Service(name='rate', path='/api/eur_usd_rate')

@rate.get()
def eur_usd_rate(request):
    contents = urllib.request.urlopen("https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml")
    xmldoc = minidom.parse(contents)
    itemlist = xmldoc.getElementsByTagName('Cube')
    for c in itemlist:
        if  c.hasAttribute('currency'):
            if c.attributes['currency'].value == 'USD':
                return dict(
                    USD=c.attributes['rate'].value
                )

    return dict(
        error="error"
    )

token = Service(name='token', path='/api/token/{token}')

@token.get()
def token_sum(request):
    token = request.matchdict['token']
    token_funds = getTokenFunds(request, token)
    
    return dict(
        token=token,
        total=token_funds.total
    )
