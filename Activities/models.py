from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so


# Base is called an Abstract Base Class - our SQL Alchemy models will inherit from this class
class Base(so.DeclarativeBase):
    pass


# Sets up a link table with activity_id and person_id as foreign keys
# Base.metadata is a container object that keeps together many different features of the database.
# Note that this table is created in the sqlalchemy layer, not in sqlalchemy.orm - it will therefore
# not be usable as a python object using the sqlalchemy ORM
person_activities = sa.Table('person_activities',
                             Base.metadata,
                             sa.Column('id', sa.Integer, primary_key=True),
                             sa.Column('activity_id', sa.ForeignKey('activities.id')),
                             sa.Column('person_id', sa.ForeignKey('persons.id')),
                             sa.UniqueConstraint('activity_id', 'person_id')
                             )


class Location(Base):
    __tablename__ = 'locations'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    room: so.Mapped[str]
    activities: so.Mapped[list["Activity"]] = so.relationship(back_populates="location")


# Sets up an Activity table, this references "attendees" via the person_activities table.
# Note that we use the 'new' SQLalchemy 2.0 method of creating columns mapped to python object attributes
# The column types are set using type hints and additional features can be added with so.mapped_column
class Activity(Base):
    __tablename__ = 'activities'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(unique=True)
    location_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('locations.id'))
    location: so.Mapped[Location] = so.relationship(back_populates="activities")

    attendees: so.Mapped[list["Person"]] = so.relationship("Person",
                                                           secondary=person_activities,
                                                           order_by='(Person.last_name, Person.first_name)',
                                                           back_populates="activities")

    # Gives a representation of an Activity (for printing out)
    def __repr__(self) -> str:
        return f"Activity(name='{self.name}')"


# Sets up a Person table, this references "activities" via the person_activities table.
# In this case we allow the first_name to be optional, so it may be Null in the database table.
# first_name and last_name do not have additional column requirements, so the type hint is sufficient
class Person(Base):
    __tablename__ = 'persons'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    first_name: so.Mapped[Optional[str]]
    last_name: so.Mapped[str]
    activities: so.Mapped[list[Activity]] = so.relationship("Activity",
                                                            secondary=person_activities,
                                                            order_by='Activity.name',
                                                            back_populates="attendees")

    # Gives a representation of a Person (for printing out)
    def __repr__(self) -> str:
        return f"Person(first_name='{self.first_name}', last_name='{self.last_name}')"

    # Include a method:
    def greeting(self) -> None:
        print(f'{self.first_name} says "hello"!')
