import sqlite3


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


    cursor.execute(parameterised_insert_query, ("Harry", "Potter", 13, "Male"))
    conn.commit()