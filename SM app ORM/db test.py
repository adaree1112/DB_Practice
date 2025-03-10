import pytest
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.exc import IntegrityError

from models import User, Post, Comment, Base

test_db_location = "sqlite:///:memory:"

def test_test():
    assert 3**2 ==9

class TestDatabase:
    @pytest.fixture(scope="class")
    def db_session(self):
        engine = sa.create_engine(test_db_location)
        Base.metadata.create_all(engine)
        session = so.Session(engine)
        yield session
        session.rollback()
        session.close()
        Base.metadata.drop_all(engine)

    def test_valid_user(self, db_session):
        user = User(name="Rayhan", age=20, gender="Male")
        db_session.add(user)
        db_session.commit()
        qry=sa.select(User).where(User.name == "Rayhan")
        rayhan = db_session.scalar(qry)

        assert rayhan is not None
        assert rayhan.name == "Rayhan"
        assert rayhan.age == 20
        assert rayhan.gender == "Male"
        assert rayhan.nationality is None

    def test_invalid_user(self, db_session):
        user = User(age=7, nationality="British")
        db_session.add(user)
        with pytest.raises(IntegrityError):
            db_session.commit()

        db_session.rollback()

    def test_valid_post(self, db_session):
        """ creating a user and add in a post to that user
        - check post is included in user.posts and the user is included it post.user"""

        user = User(name="Adam", age=20, gender="Male")

        post = Post(title="HI", description="The Game")
        user.posts.append(post)
        db_session.add(user)
        db_session.commit()
        qry=sa.select(User).where(User.name == "Adam")
        adam = db_session.scalar(qry)

        assert adam.posts == [post]
        assert adam.posts[0].description == "The Game"
        assert adam.posts[0].title == "HI"

        qry=sa.select(Post).where(Post.title == "HI")
        hi = db_session.scalar(qry)

        assert hi.user == user
        assert hi.user.name == "Adam"
        assert hi.user.age == 20