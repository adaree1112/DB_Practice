from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Person, Activity

people = [Person(first_name="Andrew", last_name="Dales"),Person(first_name="Chris", last_name="Brolin"),Person(first_name="Vera", last_name="Malcova")]

chess = Activity(name="Chess")
fives = Activity(name="Fives")
outdoor_ed = Activity(name="Outdoor Ed")

people[0].activities.append(chess)
people[0].activities.append(fives)
people[1].activities.append(outdoor_ed)
people[1].activities.append(fives)

engine = create_engine("sqlite:///activities.db",echo=True)

with Session(engine) as sess:
    sess.add_all(people)
    sess.commit()