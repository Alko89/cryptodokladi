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


class Funds(Base):
    __tablename__ = 'funds'
    id = Column(Integer, primary_key=True)
    token = Column(Text, nullable=False)
    value = Column(Numeric(precision=28, scale=18), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    comment = Column(Text)

    user_id = Column(ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='user_funds')
