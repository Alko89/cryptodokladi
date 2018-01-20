from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    String
)
from sqlalchemy.orm import relationship

from .meta import Base


class Page(Base):
    """ The SQLAlchemy declarative model class for a Page object. """
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    title = Column(Text)
    subtitle = Column(Text)
    data = Column(Text, nullable=False)

    creator_id = Column(ForeignKey('users.id'), nullable=False)
    creator = relationship('User', backref='created_pages')

# class Commetn(Base):
#     __tablename__ = 'comments'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(255))
#     data = Column(Text, nullable=False)

#     page_id = Column(ForeignKey('pages.id'), nullable=False)
#     page = relationship('Page', backref='page_comments')

#     creator_id = Column(ForeignKey('users.id'), nullable=False)
#     creator = relationship('User', backref='posted_comments')
