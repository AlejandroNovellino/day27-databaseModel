import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from eralchemy import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    # Columns for user
    id = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False)
    mail = Column(String(200), nullable=False)
    password = Column(String(200), nullable=False)
    #follower = Column(User, ForeignKey('user.id'))
    # Relation with profile, one to one
    profile = relationship('Profile', uselist=False, back_populates='user')
    # Relation with publications, one to many (bidirectional)
    publications = relationship('Publication', back_populates='user')
    # Relation with lie, one to many (bidirectional)
    likes = relationship('Likes', back_populates='user')
    # Relation with followRequest
    followers = relationship('FollowRequest', backref='followed', foreign_keys='followed')
    followeds = relationship('FollowRequest', backref='follower', foreign_keys='follower')

class Profile(Base):
    __tablename__ = 'profile'
    # Columns for profile
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    picture = Column(String(100))
    description = Column(String(1000))
    # Relation with User, many to one (bidirectional)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='profile')

class FollowRequest(Base):
    __tablename__ = 'followrequest'
    # Columns for followrequest
    id = Column(Integer, primary_key=True)
    status = Column(String(10))
    # Relation with user as follower
    follower_id = Column(Integer, ForeignKey('user.id'))
    # Relation with user as followed
    followed_id = Column(Integer, ForeignKey('user.id'))

class Publication(Base):
    __tablename__ = 'publication'
    # Columns for publication
    id = Column(Integer, primary_key=True)
    # Relation with User
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='publications')
    # Relation with Like, one to many (unidirectional)
    likes = relationship('Like')
    # Other attributes 
    message = Column(String(2000))

class Like(Base):
    __tablename__ = 'like'
    # Columns for like
    id = Column(Integer, primary_key=True)
    # Relation with Publication, no relationship from like to publication
    publication_id = Column(Integer, ForeignKey('publication.id'))
    # Relation with user, many to one (bidirectional)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='likes')

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e