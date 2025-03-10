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