import sqlite3
import faker
import random

fake = faker.Faker('en_GB')

with sqlite3.connect("student.sqlite") as conn:
    cursor=conn.cursor()

    insert_query = """
    INSERT INTO students (first_name, last_name, age, gender)
    values ('Milan','Gal',12,'Male');
    """

    parameterised_insert_query = """
    INSERT INTO students (first_name, last_name, age, gender)
    values (?,?,?,?);
    """

    fake.random.seed(4321)
    random.seed(4321)
    for _ in range(100):
        f=fake.profile()
        cursor.execute(parameterised_insert_query, [*f['name'].split(' ')[-2:], random.randint(11,40), f['sex']])

    # cursor.execute(parameterised_insert_query, ("Harry", "Potter", 13, "Male"))
    conn.commit()