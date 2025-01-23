import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Enum
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
from sqlalchemy import create_engine
from eralchemy2 import render_er

import enum

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id : Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    email : Mapped[str] = mapped_column(String(320), nullable=False)
    username : Mapped[str] = mapped_column(String(30), nullable=False)
    password : Mapped[str] = mapped_column(String(100), nullable=False)
    first_name : Mapped[str] = mapped_column(String(30), nullable=False)
    last_name : Mapped[str] = mapped_column(String(30), nullable=False)

    # https://docs.sqlalchemy.org/en/20/orm/join_conditions.html#self-referential-many-to-many-relationship
    following = relationship (
        "User",
        secondary= "followers",
        primaryjoin="Follower.follower_id==User.id",
        secondaryjoin="Follower.following_id==User.id",
        backref="followers"
    )
    posts = relationship("Post", back_populates="user_posts")
    user_comments =relationship("Comment", back_populates="user_comments")
     

class Follower(Base):
    __tablename__ = 'followers'
    id : Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)

    follower_id : Mapped[int] = mapped_column(ForeignKey('user.id'))
    followee_id : Mapped[int] = mapped_column(ForeignKey('user.id'))


class Post(Base):
    __tablename__ = 'post'
    id : Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    user_posts: Mapped["User"] = relationship("User", back_populates="posts" ,foreign_keys = user_id)
    post_comments = relationship("Comment", back_populates="post_comments")
    media_files = relationship("Media", back_populates="post")

class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    GIF = "gif"    

class Media(Base):
    __tablename__ = 'media'
    id : Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    post_id : Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="media_files")

class Comment(Base):
    __tablename__ = 'comments'
    id : Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    comment_text: Mapped[str] = mapped_column(String(600), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    user_comments: Mapped["User"] = relationship("User", back_populates="user_comments" ,foreign_keys = user_id)
    post_comments: Mapped["Post"] = relationship("Post", back_populates="post_comments" ,foreign_keys = post_id)



## Draw from SQLAlchemy base
try: 
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
