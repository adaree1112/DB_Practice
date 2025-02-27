from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Post, User, Comment

engine = create_engine('sqlite:///Sm_app.sqlite', echo=True)
session = Session(bind=engine)

"""
people = [User(name="Adam",age=16,gender="male",nationality="a"), User(name="Alex",age=18,gender="male",nationality="b"),
          User(name="Andrew",age=19,gender="male",nationality="c")]
p=Post(title="Hi",description="Hello")

comm = Comment(comment="This is a comment", user_id=2)

p.comments.append(comm)

people[0].posts.append(p)
people[1].liked_posts.append(p)
people[2].liked_posts.append(p)
"""

# Create examples of Users
users = [User(name="Alice", age=30, gender="Female", nationality="Canadian"),
         User(name="Bob", age=25, gender="Male", nationality="American"),
         User(name="Charlie", age=28, gender="Male", nationality="British"),
         User(name="Diana", age=22, gender="Female", nationality="Australian"),
         ]

# Create examples of Posts
posts = [Post(title="Exploring the Rocky Mountains",
             description="Just returned from an amazing trip to the Rockies! "
                         "The views were breathtaking and the hikes were exhilarating.",
             ),
         Post(title="My Favorite Recipes",
             description="Sharing some of my favorite recipes, including a "
                         "delicious chocolate cake and a savory lasagna."
             ),
         Post(title="Tech Innovations in 2025",
             description="Discussing the latest tech innovations, "
                         "including advancements in AI, quantum computing, and renewable energy.",
             ),
         Post(title="Travel Tips for Australia",
             description="Planning a trip to Australia? Here are some tips to make your journey unforgettable, "
                         "from must-see destinations to local cuisine."),
         ]

for i in range(len(users)):
    users[i].posts.append(posts[i])

# Add likes
users[0].liked_posts.append(posts[1])
users[0].liked_posts.append(posts[2])
users[1].liked_posts.append(posts[0])
users[1].liked_posts.append(posts[3])
users[2].liked_posts.append(posts[0])
users[2].liked_posts.append(posts[3])
users[3].liked_posts.append(posts[1])
users[3].liked_posts.append(posts[2])

session.add_all(users)
session.commit()

# Create examples of Comments
comments = [
    Comment(user_id=users[1].id, comment="Wow, the Rockies sound incredible! Thanks for sharing your experience."),
    Comment(user_id=users[2].id, comment="I'd love to go to the Rockies."),
    Comment(user_id=users[2].id, comment="I tried the chocolate cake recipe, and it was a hit! Thanks for the great recipe."),
    Comment(user_id=users[3].id, comment="Fascinating insights on tech innovations. Can't wait to see what the future holds!"),
    Comment(user_id=users[0].id, comment="Great tips for traveling in Australia. I'll definitely keep these in mind for my next trip.")
]

posts[0].comments.append(comments[0])
posts[0].comments.append(comments[1])
posts[1].comments.append(comments[2])
posts[2].comments.append(comments[3])
posts[3].comments.append(comments[4])

session.add_all(comments)
session.commit()

