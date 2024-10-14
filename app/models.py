from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase 
from .database import Base
from sqlalchemy.orm import Mapped, mapped_column
# Many to many relationship between posts and tags.
post_tags = Table(
    'post_tags',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('post.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True)
)

class Post(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    status: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    # Relationship with User - Belongs to a User
    post_owner = relationship("User", back_populates="posts")

    # Relationship with Comment - Has many Comments
    comments = relationship("Comment", back_populates="comment_belongs_to_post")

    # Relationship with Tags - Has many Tags
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")

class Comment(Base):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    
    # Relationship with Post - Belongs to a Post
    comment_belongs_to_post = relationship("Post", back_populates="comments")

    # Relationship with User - Belongs to a User
    comment_owner = relationship("User", back_populates="comments")

class Tag(Base):
    __tablename__ = "tag"
    id: Mapped[int] = mapped_column(primary_key=True)
    tag_name: Mapped[str] = mapped_column(unique=True)
    
    # Relationship with Posts - Has many Posts
    posts = relationship("Post", secondary=post_tags, back_populates="tags")

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)

    # Relationship with Comment - Has many Comments
    comments = relationship("Comment", back_populates="comment_owner")

    # Relationship with Post - Has many Posts
    posts = relationship("Post", back_populates="post_owner")
