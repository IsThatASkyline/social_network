from datetime import datetime
from sqlalchemy.orm import relationship, column_property
from src.auth.models import User
from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, select, func
from src.database import Base


class PostsDislikes(Base):
    __tablename__ = 'posts_dislikes'

    id: int = Column(Integer, primary_key=True)
    post_id: int = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'))
    post = relationship("Post")
    user_id: int = Column(Integer, ForeignKey(User.id))
    user = relationship("User")


class PostsLikes(Base):
    __tablename__ = 'posts_likes'

    id: int = Column(Integer, primary_key=True)
    post_id: int = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'))
    post = relationship("Post")
    user_id: int = Column(Integer, ForeignKey(User.id))
    user = relationship("User")


class Post(Base):
    __tablename__ = 'posts'

    id: int = Column(Integer, primary_key=True)
    text: str = Column(String(length=500))
    owner_id: int = Column(Integer, ForeignKey(User.id))
    owner = relationship("User", backref='posts')
    likes_amount = column_property(select(func.count(PostsLikes.id)).where(PostsLikes.post_id == id).scalar_subquery())
    dislikes_amount = column_property(select(func.count(PostsDislikes.id)).where(PostsDislikes.post_id == id).scalar_subquery())
    created_at = Column(TIMESTAMP, default=datetime.utcnow())
