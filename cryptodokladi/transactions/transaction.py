from ..models import Funds

from sqlalchemy import func, union


def transaction(request, token, value, comment, sending_user, receiving_user):
    """Sends the value of a token from sending_user to reciving_user

    Arguments:
        request {[type]} -- [description]
        token {string} -- Token to be sent
        value {int} -- Value of tokens to be sent
        comment {string} -- Optional comment
        sending_user {User} -- Sender
        receiving_user {User} -- Reciever
    """
    fund_receive = Funds(token=token, value=value, comment=comment, user=receiving_user, sender=sending_user)
    request.dbsession.add(fund_receive)

def getTransactions(request, user, token):
    """Get token transactions of a user

    Arguments:
        request {[type]} -- [description]
        user {User} -- User
        token {string} -- Token currency code

    Returns:
        Funds -- List of user transactions per token
    """
    transactions_btc_r = request.dbsession.query(Funds).filter_by(user=user).filter(Funds.token==token)
    transactions_btc_s = request.dbsession.query(Funds).filter_by(sender=user).filter(Funds.token==token)
    return transactions_btc_r.union(transactions_btc_s)

def getTokenSums(request, user):
    """Gets the sums of tokens for a user

    Arguments:
        request {[type]} -- [description]
        user {User} -- User

    Returns:
        list -- Sums of all token funds of a User
    """
    tokens_r = request.dbsession.query(Funds.token.label('token'), func.sum(Funds.value).label('value')).filter_by(user=user).group_by(Funds.token)
    tokens_s = request.dbsession.query(Funds.token.label('token'), -func.sum(Funds.value).label('value')).filter_by(sender=user).group_by(Funds.token)
    tokens_u = union(tokens_r, tokens_s).alias('funds')
    return request.dbsession.query(tokens_u.columns.token, func.sum(tokens_u.columns.value).label('value')).group_by(Funds.token)


def getTokenSum(request, user, token):
    """Get the sum of a token for a user

    Arguments:
        request {[type]} -- [description]
        user {User} -- User
        token {string} -- Token currency code

    Returns:
        list -- Sum of token funds of a User
    """
    tokens_r = request.dbsession.query(Funds.token.label('token'), func.sum(Funds.value).label('value')).filter_by(user=user).filter(Funds.token==token)
    tokens_s = request.dbsession.query(Funds.token.label('token'), -func.sum(Funds.value).label('value')).filter_by(sender=user).filter(Funds.token==token)
    tokens_u = union(tokens_r, tokens_s).alias('funds')
    return request.dbsession.query(tokens_u.columns.token, func.sum(tokens_u.columns.value).label('value'))


def getTokenFunds(request, token):
    """Get the sum of a token

    Arguments:
        request {[type]} -- [description]
        token {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    token_r = request.dbsession.query(Funds.token.label('token'), func.sum(Funds.value).label('total')).filter(Funds.token==token).group_by(Funds.user_id)
    token_s = request.dbsession.query(Funds.token.label('token'), func.sum(-Funds.value).label('total')).filter(Funds.token==token).filter(Funds.sender_id.isnot(None))
    token_u = union(token_r, token_s).alias('total')
    return request.dbsession.query(token_u.columns.token, func.sum(token_u.columns.total).label('total')).first()

def getTokenUserFunds(request, token):
    """Get the sum of a token for all users

    Arguments:
        request {[type]} -- [description]
        token {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    users_r = request.dbsession.query(Funds.user_id.label('user_id'), func.sum(Funds.value).label("total")).filter(Funds.token==token).group_by(Funds.user_id)
    users_s = request.dbsession.query(Funds.sender_id.label('user_id'), func.sum(-Funds.value).label("total")).filter(Funds.sender_id.isnot(None)).filter(Funds.token==token).group_by(Funds.sender_id)
    users_u = union(users_r, users_s).alias('total')
    return request.dbsession.query(users_u.columns.user_id, func.sum(users_u.columns.total).label('total')).group_by(users_u.columns.user_id)
