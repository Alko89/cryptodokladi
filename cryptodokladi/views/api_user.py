from cornice import Service
from cornice.validators import marshmallow_body_validator

from ..rules import ( send_funds_factory )
from ..models import User, UserSchema

import json

user_schema = UserSchema()


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
