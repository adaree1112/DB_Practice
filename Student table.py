import sqlite3

conn=sqlite3.connect("student.sqlite")
cursor = conn.cursor()
create_student_table= """
CREATE TABLE students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
age INTEGER,
gender TEXT
);"""

cursor.execute(create_student_table)

conn.commit()
conn.close()