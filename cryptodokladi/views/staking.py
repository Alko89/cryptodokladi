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

@view_config(route_name='calculate_staking_rewards', renderer='json')
def calculate_staking_rewards(request):
    pivx_reward = float(request.matchdict['pivx_reward'])

    #SELECT SUM(value) FROM funds WHERE token = 'PIVX';
    pivx_funds = request.dbsession.query(func.sum(Funds.value).label("total")).filter(Funds.token=="PIVX").first()
    pivx_user_funds = request.dbsession.query(func.sum(Funds.value).label("total")).filter(Funds.token=="PIVX").group_by(Funds.user_id)

    pivx_user_rewards = []
    reward_sum = 0

    for total in pivx_user_funds:
        reward = (float(total[0]) * pivx_reward) / float(pivx_funds.total)
        reward_sum += reward
        pivx_user_rewards.append({'reward': reward})

    pivx_user_rewards.append({'sum': reward_sum})
    return pivx_user_rewards
