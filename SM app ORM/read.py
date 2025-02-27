from sqlalchemy import create_engine,select
from sqlalchemy.orm import Session
from models import User, Post, Comment, Base

engine = create_engine('sqlite:///Sm_app.sqlite')
session = Session(bind=engine)

# Query and print all users
users = session.scalars(select(User)).all()
for user in users:
    print(user)

# Query and print all posts
posts = session.scalars(select(Post)).all()
for post in posts:
    print(post)

# Query and print all comments
comments = session.scalars(select(Comment)).all()
for comment in comments:
    print(comment)
