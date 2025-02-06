from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from Models import Post, User

people = [User(name="Adam",age=16,gender="male",nationality="a"), User(name="Alex",age=18,gender="male",nationality="b"),
          User(name="Andrew",age=19,gender="male",nationality="c")]
p=Post(title="Hi",description="Hello")
people[0].posts.append(p)
people[1].liked_posts.append(p)
people[2].liked_posts.append(p)


engine = create_engine('sqlite:///Sm_app.sqlite',echo=True)

with Session(engine) as sess:
    sess.add_all(people)
    sess.commit()

