import sqlite3

with sqlite3.connect("student.sqlite") as conn:
    cursor = conn.cursor()
    select_students= """
    select id, first_name, last_name
    from students
    where age>15
    """

    average_query="""
    SELECT avg(age) 
    FROM students
    WHERE gender=?
    """

    cursor.execute(select_students)
    first_student = cursor.fetchone()
    more_students = cursor.fetchmany(10)
    other_students = cursor.fetchall()

    avgage=cursor.execute(average_query,('F',)).fetchone()[0]

    group_by_query = """
    Select gender, avg(age) 
    FROM students
    GROUP BY gender
    """
    grouped=cursor.execute(group_by_query,).fetchall()

    select_j= """
    select id,first_name,last_name,gender
    from students
    where first_name like 'J%'"""

    cursor.execute(select_j)
    first_five=cursor.fetchmany(5)

    count_gender="""
    select count(*)
    from students
    group by gender"""

    sum_by_letter="""
    select sum(age)
    from students
    group by substr(first_name, 1, 1);
    """
