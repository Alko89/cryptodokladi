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

from .user import transaction, getTokenSums

@view_config(route_name='limit_trade', renderer='../templates/limit_trade.jinja2', permission='send')
def limit_trade(request):
    user = request.user
    trades = request.dbsession.query(LimitTrade).filter(LimitTrade.user != user).order_by(LimitTrade.timestamp.desc())
    user_trades = request.dbsession.query(LimitTrade).filter(LimitTrade.user == user)
    tokens = getTokenSums(request, user)

    if 'form.submitted' in request.params:
        buy_token = request.params['buy_token']
        sell_token = request.params['sell_token']
        value = request.params['value']
        rate = request.params['rate']
        buysell = request.params['buysell']

        # check maching pair with the same rate and remember who is buying and who is selling
        buynotsell = False
        if buysell == 'buy':
            matching_trades = request.dbsession.query(LimitTrade).filter(
                LimitTrade.buy_token == buy_token,
                LimitTrade.sell_token == sell_token,
                LimitTrade.rate == rate,
                LimitTrade.buysell == 'sell',
                LimitTrade.user != user
            ).order_by(LimitTrade.timestamp.asc())
            buynotsell = True
        elif buysell == 'sell':
            matching_trades = request.dbsession.query(LimitTrade).filter(
                LimitTrade.buy_token == buy_token,
                LimitTrade.sell_token == sell_token,
                LimitTrade.rate == rate,
                LimitTrade.buysell == 'buy',
                LimitTrade.user != user
            ).order_by(LimitTrade.timestamp.asc())
            buynotsell = False
        else:
            next_url = request.route_url('limit_trade')
            return HTTPFound(location=next_url)
        
        trade = LimitTrade(buy_token=buy_token, sell_token=sell_token, value=value, rate=rate, buysell=buysell, user=user)
        request.dbsession.add(trade)

        for match in matching_trades:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!MATCH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            if buynotsell:
                want_buy = float(trade.value) * float(trade.rate)
                can_sell = float(match.value) * float(match.rate)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!BUY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(want_buy)
                print(can_sell)

                # if the user wants to buy more than its match can sell, then buy all and try another match
                if want_buy > can_sell:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!want_buy > can_sell!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    trade.value = float(trade.value) - float(match.value)
                    print(trade.value)
                    #transaction(request, token, value, comment, sending_user, receiving_user)
                    transaction(request, buy_token, match.value, buy_token + sell_token + 'buy', match.user, user)
                    transaction(request, sell_token, can_sell, buy_token + sell_token + 'sell', user, match.user)

                    request.dbsession.delete(match)

                    continue
                # if the user wants to buy less, buy as much as possible and break
                elif want_buy < can_sell:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!want_buy < can_sell!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    match.value = float(match.value) - float(trade.value)
                    print(match.value)

                    transaction(request, buy_token, trade.value, buy_token + sell_token + 'buy', match.user, user)
                    transaction(request, sell_token, want_buy, buy_token + sell_token, user + 'sell', match.user)

                    request.dbsession.delete(trade)
                    break
                # a perfect world
                else:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!a perfect buy!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    transaction(request, buy_token, trade.value, buy_token + sell_token + 'buy', match.user, user)
                    transaction(request, sell_token, can_sell, buy_token + sell_token + 'sell', user, match.user)

                    request.dbsession.delete(match)
                    request.dbsession.delete(trade)

                    break
            else:
                want_sell = float(trade.value) * float(trade.rate)
                can_buy = float(match.value) * float(match.rate)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!SELL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(want_sell)
                print(can_buy)

                # if the user wants to sell more than its match can buy, then sell all and try another match
                if want_sell > can_buy:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!want_sell > can_buy!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    trade.value = float(trade.value) - float(match.value)
                    print(trade.value)
                    #transaction(request, token, value, comment, sending_user, receiving_user)
                    transaction(request, buy_token, match.value, buy_token + sell_token + 'sell', user, match.user)
                    transaction(request, sell_token, can_buy, buy_token + sell_token + 'buy', match.user, user)

                    request.dbsession.delete(match)

                    continue
                # if the user wants to buy less, sell as much as possible and break
                elif want_sell < can_buy:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!want_sell < can_buy!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    match.value = float(match.value) - float(trade.value)
                    print(match.value)

                    transaction(request, buy_token, trade.value, buy_token + sell_token + 'sell', user, match.user)
                    transaction(request, sell_token, want_sell, buy_token + sell_token + 'buy', match.user, user)

                    request.dbsession.delete(trade)
                
                    break
                # a perfect world
                else:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!a perfect sell!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    transaction(request, buy_token, trade.value, buy_token + sell_token + 'sell', user, match.user)
                    transaction(request, sell_token, want_sell, buy_token + sell_token + 'buy', match.user, user)

                    request.dbsession.delete(match)
                    request.dbsession.delete(trade)

                    break


        next_url = request.route_url('limit_trade')
        return HTTPFound(location=next_url)

    return dict(
        user=user,
        tokens=tokens,
        trades=trades,
        user_trades=user_trades
    )
