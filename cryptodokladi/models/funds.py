from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
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
    value = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user_id = Column(ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='user_funds')
