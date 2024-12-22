from backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    login = Column(String(40), unique=True,index=True)
    email = Column(String(40), unique=True,index=True)
    password = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)
    game = relationship('Game', back_populates='user')

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    age_limited = Column(Boolean, default=False)
    cost = Column(Float)
    size = Column(Float)
    slug = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)