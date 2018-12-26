import bcrypt
from sqlalchemy import (
    Column,
    Integer,
    Text,
    String
)

from .meta import Base
from marshmallow_sqlalchemy import ModelSchema


class User(Base):
    """ The SQLAlchemy declarative model class for a User object. """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    role = Column(String(255), nullable=False)

    password_hash = Column(Text)

    email = Column(String(255))
    firstname = Column(String(255))
    lastname = Column(String(255))
    address = Column(Text)
    city = Column(String(255))
    postalcode = Column(Integer)
    country = Column(String(255))
    about = Column(Text)

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password_hash = pwhash

    def check_password(self, pw):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False

class UserSchema(ModelSchema):
    class Meta:
        model = User
