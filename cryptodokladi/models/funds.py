from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    String,
    DateTime
)
from sqlalchemy.orm import relationship

from datetime import datetime

from .meta import Base


class Funds(Base):
    __tablename__ = 'funds'
    __table_args__ = {'extend_existing': True} 
    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    comment = Column(Text)

    user_id = Column(ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='user_funds')

    token_id = Column(ForeignKey('tokens.id'), nullable=False)
    token = relationship('Token', backref='base_token')


class Token(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    token = Column(String(255),  nullable=False)
    name = Column(String(255),  nullable=False)
    unit = Column(String(255),  nullable=False)
    base = Column(Integer, nullable=False)
