import pytest
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.exc import IntegrityError

from models import User, Post, Comment, Base
from write import write_initial_data
from app import Controller

test_db_location = "sqlite:///test_database.db"


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
        qry = sa.select(User).where(User.name == "Rayhan")
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
        user = User(name="Adam", age=20, gender="Male")
        post = Post(title="HI", description="The Game")
        user.posts.append(post)
        db_session.add(user)
        db_session.commit()

        qry = sa.select(User).where(User.name == "Adam")
        adam = db_session.scalar(qry)

        assert adam.posts == [post]
        assert adam.posts[0].description == "The Game"
        assert adam.posts[0].title == "HI"

        qry = sa.select(Post).where(Post.title == "HI")
        hi = db_session.scalar(qry)

        assert hi.user == user
        assert hi.user.name == "Adam"
        assert hi.user.age == 20

    def test_user_can_comment_on_post(self, db_session):
        user = User(name="John", age=25, gender="Male")
        post = Post(title="Test Post", description="Testing comments")
        db_session.add_all([user, post])
        db_session.commit()

        comment = Comment(user_id=user.id, post_id=post.id, comment="Nice post!")
        db_session.add(comment)
        db_session.commit()

        qry = sa.select(Comment).where(Comment.user_id == user.id, Comment.post_id == post.id)
        fetched_comment = db_session.scalar(qry)

        assert fetched_comment is not None
        assert fetched_comment.comment == "Nice post!"
        assert fetched_comment.user == user
        assert fetched_comment.post == post

    def test_user_can_like_post(self, db_session):
        user = User(name="Alice", age=30, gender="Female")
        post = Post(title="Like Test", description="Testing likes")
        db_session.add_all([user, post])
        db_session.commit()

        user.liked_posts.append(post)
        db_session.commit()

        qry = sa.select(User).where(User.name == "Alice")
        alice = db_session.scalar(qry)

        assert post in alice.liked_posts
        assert alice in post.liked_by_user

    def test_user_cannot_like_post_twice(self, db_session):
        user = User(name="Bob", age=22, gender="Male")
        post = Post(title="Duplicate Like Test", description="Testing duplicate likes")
        db_session.add_all([user, post])
        db_session.commit()

        user.liked_posts.append(post)
        db_session.commit()

        user.liked_posts.append(post)
        db_session.add(user)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()


class TestController:
    @pytest.fixture(scope="class",autouse=True)
    def test_db(self):
        engine = sa.create_engine(test_db_location)
        Base.metadata.create_all(engine)
        write_initial_data(engine)
        yield
        Base.metadata.drop_all(engine)
    @pytest.fixture(scope="class")
    def controller(self):
        return Controller(db_location=test_db_location)


    def test_set_current_user_from_name(self,controller):
        controller.set_current_user_from_name("Alice")
        assert controller.current_user.name == "Alice"
        assert controller.current_user.gender == "Female"
        assert controller.current_user.id == 1
        assert controller.current_user.age == 30

    def test_get_user_names(self,controller):
        user_names = controller.get_user_names()
        assert user_names == ["Alice", "Bob", "Charlie", "Diana"]

    def test_create_user(self, controller):
        user = controller.create_user(name="Eve", age=27, gender="Female", nationality="German")

        assert user is not None
        assert user.name == "Eve"
        assert user.age == 27
        assert user.gender == "Female"
        assert user.nationality == "German"

        user_names = controller.get_user_names()
        assert "Eve" in user_names

    def test_create_post(self, controller):
        controller.set_current_user_from_name("Alice")
        post = controller.create_post(title="A Day at the Beach", description="Had an amazing time at the beach today!")

        assert post is not None
        assert post.title == "A Day at the Beach"
        assert post.description == "Had an amazing time at the beach today!"
        assert post.user_id is not None

        posts = controller.get_posts("Alice")
        assert any(p["title"] == "A Day at the Beach" for p in posts)

    def test_get_current_user(self, controller):
        controller.set_current_user_from_name("Alice")
        user = controller.get_current_user()

        assert user is not None
        assert user.name == "Alice"
        assert user.age == 30
        assert user.gender == "Female"
        assert user.nationality == "Canadian"

    def test_get_posts(self, controller):
        controller.set_current_user_from_name("Alice")

        controller.create_post(title="Alice's Adventure", description="A story about Alice's travels.")

        posts = controller.get_posts("Alice")

        assert len(posts) > 0
        assert any(
            p["title"] == "Alice's Adventure" and p["description"] == "A story about Alice's travels." for p in posts)

    def test_add_comment(self, controller):
        controller.set_current_user_from_name("Alice")

        post = controller.create_post(title="Alice's Adventure", description="A story about Alice's travels.")

        controller.add_comment(post_id=post.id, comment_text="What a fantastic adventure, Alice!")

        posts = controller.get_posts("Alice")
        assert len(posts) > 0
        post_info = next(p for p in posts if p["id"] == post.id)
        assert any(comment["comment"] == "What a fantastic adventure, Alice!" for comment in post_info["comments"])
