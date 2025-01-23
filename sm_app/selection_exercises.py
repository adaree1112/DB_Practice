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

ex3= """
Select name, count(posts.id)
from users
inner join posts on users.id = posts.user_id
group by users.id"""

ex4 = """
Select name, comments.text as text
from users
inner join comments on users.id = comments.user_id
"""


with sqlite3.connect('sm_app.sqlite') as conn:
    ex1_headers,ex1_data = execute_read_query(conn,ex1)
    print(tabulate(ex1_data,headers=ex1_headers,tablefmt='psql'))

    cur=conn.cursor()
    cur.execute(ex2)

    ex3_headers,ex3_data = execute_read_query(conn,ex3)
    print(tabulate(ex3_data,headers=ex3_headers,tablefmt='psql'))

    ex4_headers,ex4_data = execute_read_query(conn,ex4)
    print(tabulate(ex4_data,headers=ex4_headers,tablefmt='psql'))