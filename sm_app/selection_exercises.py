import sqlite3
from tabulate import tabulate

def execute_read_query(connection,query):
    cursor = connection.cursor()
    result = None

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        return column_names, result
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")

ex1= """
Select text 
from comments
where text like '%?'
"""

ex2= """
Update users
set name='Lizzy'
where name = 'Elizabeth'
"""


with sqlite3.connect('sm_app.sqlite') as conn:
    ex1_headers,ex1_data = execute_read_query(conn,ex1)
    print(tabulate(ex1_data,headers=ex1_headers,tablefmt='psql'))

    cur=conn.cursor()
    cur.execute(ex2)

