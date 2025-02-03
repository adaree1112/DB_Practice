from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so

#abstract base class
class Base(so.DeclarativeBase):
    pass
person_activities = sa.Table("person_activities",
                             Base.metadata,
                             sa.Column("id", sa.Integer,primary_key=True,autoincrement=True),
                             sa.Column("activity_id",sa.ForeignKey("activities.id",)),
                             sa.Column("person_id",sa.ForeignKey("persons.id"),),
                             sa.UniqueConstraint("activity_id","person_id")
                             )
class Activity(Base):
    __tablename__ = "activities"
    id: so.Mapped[int] = so.mapped_column(primary_key=True,autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(unique=True)
    attendees: so.Mapped[list["Person"]] = so.relationship("Person", secondary=person_activities, order_by="(Person.last_name, Person.first_name)",back_populates="activities")
    def __repr__(self) -> str:
        return f"Activity(name='{self.name}')"

class Person(Base):
    __tablename__ = 'persons'
    id: so.Mapped[int] = so.mapped_column(primary_key=True,autoincrement=True)
    first_name: so.Mapped[Optional[str]]
    last_name: so.Mapped[str]
    activities: so.Mapped [list[Activity]] = so.relationship("Activity", secondary=person_activities, order_by=Activity.name,back_populates="attendees")

    def __repr__(self) -> str:
        return f'Person({self.first_name} {self.last_name})'

    def greeting(self) -> None:
        print(f"{self.first_name} says 'Hello'")


