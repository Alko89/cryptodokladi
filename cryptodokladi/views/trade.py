from pyramid.compat import escape
import re
from docutils.core import publish_parts

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
)

from pyramid.view import view_config
from sqlalchemy import func, union, select

from ..models import User, Funds, LimitTrade

@view_config(route_name='limit_trade', renderer='../templates/limit_trade.jinja2', permission='send')
def limit_trade(request):
    user = request.user
    trades = request.dbsession.query(LimitTrade)
    user_trades = request.dbsession.query(LimitTrade).filter_by(user=user)

    if 'form.submitted' in request.params:
        buy_token = request.params['buy_token']
        sell_token = request.params['sell_token']
        value = request.params['value']
        rate = request.params['rate']
        buysell = request.params['buysell']

        trade = LimitTrade(buy_token=buy_token, sell_token=sell_token, value=value, rate=rate, buysell=buysell, user=user)
        request.dbsession.add(trade)

        next_url = request.route_url('limit_trade')
        return HTTPFound(location=next_url)

    return dict(user=user, trades=trades, user_trades=user_trades)
