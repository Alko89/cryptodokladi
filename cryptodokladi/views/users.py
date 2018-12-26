from cornice import Service
from cornice.validators import marshmallow_body_validator

from ..rules import ( user_factory, send_funds_factory )
from ..models import User, UserSchema
from ..transactions.transaction import getTransactions

import json

user_schema = UserSchema()

transactions = Service(name='transactions', path='/api/transactions/{username}/{token}', factory=user_factory)

@transactions.get(permission="view")
def get_tokens(request):
    username = request.matchdict['username']
    user = request.dbsession.query(User).filter_by(name=username).first()
    token = request.matchdict['token']

    t = []
    for row in getTransactions(request, user, token):
        t.append({
            'token': row.token,
            'value': float(row.value),
            'timestamp': str(row.timestamp),
            'comment': row.comment,
            'user': row.user.name,
            'sender': row.sender.name if row.sender else ""
        })
    return t


user = Service(name='user', path='/api/user', factory=send_funds_factory)

@user.get(permission="view")
def get_user(request):
    user = request.user
    
    return user_schema.dump(user).data

@user.post(permission="view")
def update_user(request):
    user = request.user

    # user_sc = user_schema.load(request.body, request.dbsession, instance=user).data
    body = request.json_body

    user.email = body['email']
    user.firstname = body['firstname']
    user.lastname = body['lastname']
    user.address = body['address']
    user.city = body['city']
    user.postalcode = body['postalcode']
    user.country = body['country']
    user.about = body['about']

    return {}
