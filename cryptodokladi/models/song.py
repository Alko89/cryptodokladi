from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    Text,
    String
)

from sqlalchemy.orm import relationship

from .meta import Base


songs_tags = Table('tags', Base.metadata,
    Column('song_id', Integer, ForeignKey('song.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

class Song(Base):
    __tablename__ = 'song'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, unique=True)
    subtitle = Column(Text)
    url = Column(Text)
    ytplayer = Column(Text)
    
    tags = relationship(
        "Tag",
        secondary=songs_tags,
        back_populates="songs")

class Lyric(Base):
    __tablename__ = 'lyric'
    id = Column(Integer, primary_key=True)
    language = Column(Text, nullable=False)
    text = Column(Text, nullable=False)
    
    song_id = Column(ForeignKey("song.id"), nullable=False)
    song = relationship('Song', backref='lyrics')

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    
    songs = relationship(
        "Song",
        secondary=songs_tags,
        back_populates="tags")
