import sqlite3
with sqlite3.connect("student.sqlite") as conn:
    cursor=conn.cursor()
    update_query="""
    UPDATE students
    SET last_name=? 
    WHERE id=4
    """

    increment_age_query= """
    UPDATE students
    set age=age+?"""
    cursor.execute(update_query,('Smith',))
    cursor.execute(increment_age_query,(-1,))
    conn.commit()