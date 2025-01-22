from backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, PrimaryKeyConstraint
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String(40), unique=True, index=True)
    hashed_password = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)
    games = relationship("Game", secondary="gameusers", back_populates='users')

    def __str__(self):
        return self.username


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    age_limited = Column(Boolean, default=False)
    cost = Column(Float)
    size = Column(Float)
    slug = Column(String, unique=True, index=True)
    users = relationship("User", secondary="gameusers", back_populates='games')

    def __str__(self):
        return self.title


class GameUser(Base):
    __tablename__ = 'gameusers'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'game_id'),
    )

    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    game_id = Column(Integer, ForeignKey('games.id'), index=True)
