from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so


class Base(so.DeclarativeBase):
    pass

like = sa.Table('Likes',
                Base.metadata,
                sa.Column('id', sa.Integer, primary_key=True),
                sa.Column('user_id', sa.ForeignKey('users.id')),
                sa.Column('post_id', sa.ForeignKey('posts.id')),
                sa.UniqueConstraint('user_id', 'post_id')
                )

class User(Base):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str]
    age: so.Mapped[int]
    gender: so.Mapped[Optional[str]]
    nationality: so.Mapped[Optional[str]]
    posts: so.Mapped[list["Post"]] = so.relationship("Post",back_populates="user")
    liked_posts: so.Mapped[list["Post"]] = so.relationship("Post",
                                                           secondary=like,
                                                           order_by='Post.title',
                                                           back_populates="liked_by_user")
    #comments

class Post(Base):
    __tablename__ = 'posts'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    title: so.Mapped[str]
    description: so.Mapped[str]
    user_id: so.Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey('users.id'))

    user: so.Mapped[User] = so.relationship('User', back_populates='posts')
    liked_by_user: so.Mapped[list[User]] = so.relationship("User",
                                                           secondary=like,
                                                           order_by='User.name',
                                                           back_populates="liked_posts",
                                                           )
    #comments
#
# class Comment:
#     __tablename__ = 'comments'
#     id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
#     user_id: sa.ForeignKey(User.id)
#     post_id: sa.ForeignKey(Post.id)
#     comment: so.Mapped[str]
#     #post