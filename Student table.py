import sqlite3

conn=sqlite3.connect("student.sqlite")
cursor = conn.cursor()
create_student_table= """
CREATE TABLE IF NOT EXISTS student (
id INTEGER PRIMARY KEY AUTOINCREMENT,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
age INTEGER,
gender TEXT
);"""


conn.commit()
conn.close()