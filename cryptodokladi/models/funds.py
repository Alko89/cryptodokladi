from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    DateTime
)
from sqlalchemy.orm import relationship

from datetime import datetime

from .meta import Base
from marshmallow_sqlalchemy import ModelSchema


class Funds(Base):
    __tablename__ = 'funds'
    id = Column(Integer, primary_key=True)
    
    token = Column(Text, nullable=False)
    # token_id = Column(ForeignKey('token.id'), nullable=False)
    # token = relationship('Token', backref='token_funds', foreign_keys='Funds.token_id')

    value = Column(Numeric(precision=28, scale=18), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    comment = Column(Text)

    user_id = Column(ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='user_funds', foreign_keys='Funds.user_id')

    sender_id = Column(ForeignKey('users.id'))
    sender = relationship('User', backref='user_sender', foreign_keys='Funds.sender_id')

class FundsSchema(ModelSchema):
    class Meta:
        model = Funds


class Token(Base):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    token = Column(Text, nullable=False)

class TokenSchema(ModelSchema):
    class Meta:
        model = Token


class Rewards(Base):
    __tablename__ = 'rewards'
    id = Column(Integer, primary_key=True)

    token_id = Column(ForeignKey('token.id'), nullable=False)
    token = relationship('Token', backref='token_rewards', foreign_keys='Rewards.token_id')

    value = Column(Numeric(precision=28, scale=18), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class LimitTrade(Base):
    __tablename__ = 'limittrade'
    id = Column(Integer, primary_key=True)
    buy_token = Column(Text, nullable=False)
    sell_token = Column(Text, nullable=False)
    value = Column(Numeric(precision=28, scale=18), nullable=False)
    rate = Column(Numeric(precision=28, scale=18), nullable=False)
    buysell = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user_id = Column(ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='user_limittrade', foreign_keys='LimitTrade.user_id')
