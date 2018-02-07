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

@view_config(route_name='calculate_staking_rewards', renderer='json', permission='calc')
def calculate_staking_rewards(request):
    pivx_reward = float(request.matchdict['pivx_reward'])

    pivx_funds = request.dbsession.query(func.sum(Funds.value).label("total")).filter(Funds.token=="PIVX").first()
    pivx_user_funds = request.dbsession.query(Funds.user_id, func.sum(Funds.value).label("total")).filter(Funds.token=="PIVX").group_by(Funds.user_id)

    pivx_user_rewards = []
    reward_sum = 0

    for user in pivx_user_funds:
        reward = (float(user.total) * pivx_reward) / float(pivx_funds.total)
        reward_sum += reward

        if request.matchdict['save'] == "1":
            fund = Funds(token="PIVX", value=reward, comment="reward", user_id=user.user_id)
            request.dbsession.add(fund)

        username = request.dbsession.query(User.name).filter_by(id=user.user_id).first()

        pivx_user_rewards.append({
            'user': username,
            'reward': reward,
            'before': float(user.total),
            'after': float(user.total) + reward
        })

    pivx_user_rewards.append({'sum': reward_sum})
    return pivx_user_rewards
