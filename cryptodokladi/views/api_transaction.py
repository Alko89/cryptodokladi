from cornice import Service
from cornice.validators import marshmallow_body_validator

from ..rules import ( user_factory, send_funds_factory )
from ..models import Funds, FundsSchema, Token, TokenSchema
from ..transactions.transaction import getTransactions

import json

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
