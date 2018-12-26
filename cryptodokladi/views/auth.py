from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.view import (
    forbidden_view_config,
    view_config,
)

from ..models import User, UserSchema


user_schema = UserSchema()

@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):
    next_url = request.params.get('next', request.referrer)
    if not next_url:
        next_url = request.route_url('view_wiki')
    message = ''
    login = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        user = request.dbsession.query(User).filter_by(name=login).first()
        if user is not None and user.check_password(password):
            headers = remember(request, user.id)
            return HTTPFound(location=request.route_url('user_view', username=user.name), headers=headers)
        message = 'Failed login'

    return dict(
        message=message,
        url=request.route_url('login'),
        next_url=next_url,
        login=login,
        )

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    next_url = request.route_url('view_wiki')
    return HTTPFound(location=next_url, headers=headers)

@forbidden_view_config()
def forbidden_view(request):
    next_url = request.route_url('login', _query={'next': request.url})
    return HTTPFound(location=next_url)


@view_config(route_name='api_login', request_method='POST', renderer='json')
def api_login(request):
    """
    Temporary login for the new API this one is to be used during the
    transitional period. This method is used in Vuex store.
    Consider using JWT (https://github.com/wichert/pyramid_jwt) not
    compatible with old UI.
    """
    body = request.json_body
    login = body['email']
    password = body['password']
    user = request.dbsession.query(User).filter_by(name=login).first()
    if user is not None and user.check_password(password):
        headers = remember(request, user.id)
        request.response.headers = headers
        return {
            'result': 'ok',
            'user': user_schema.dump(user).data,
            # 'token': request.create_jwt_token(user.id)
        }
    else:
        return {
            'result': 'error'
        }
