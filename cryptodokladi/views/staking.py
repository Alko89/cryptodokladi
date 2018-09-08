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
from ..transactions.transaction import getTokenFunds, getTokenUserFunds, getTokenSum


@view_config(route_name='calculate_staking_rewards', renderer='json', permission='calc')
def calculate_staking_rewards(request):
    pivx_reward = float(request.matchdict['pivx_reward'])

    pivx_funds = getTokenFunds(request, "PIVX")
    pivx_user_funds = getTokenUserFunds(request, "PIVX")

    pivx_user_rewards = []
    reward_sum = 0
    funds_sum_after = 0

    for user in pivx_user_funds:
        reward = (float(user.total) * pivx_reward) / float(pivx_funds.total)
        reward_sum += reward
        funds_sum_after += float(user.total) + reward

        if request.matchdict['save'] == "save":
            fund = Funds(token="PIVX", value=reward, comment="reward", user_id=user.user_id)
            request.dbsession.add(fund)

        username = request.dbsession.query(User.name).filter_by(id=user.user_id).first()

        pivx_user_rewards.append({
            'user': username,
            'reward': reward,
            'before': float(user.total),
            'after': float(user.total) + reward
        })

    pivx_user_rewards.append({
        'sum': reward_sum,
        'before': float(pivx_funds.total),
        'after': funds_sum_after
    })
    return pivx_user_rewards
