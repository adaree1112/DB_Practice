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

select_users = "SELECT * FROM users"
select_posts = "SELECT * FROM posts"

select_users_posts= """
SELECT users.id, users.name, posts.description
FROM posts
INNER JOIN users ON posts.user_id = users.id
"""

select_posts_comments_users= """
Select posts.description as post, text as comment, name
FROM posts
Inner JOIN users ON posts.user_id = users.id
INNER JOIN comments ON posts.id = comments.post_id
"""

select_post_likes="""
SELECT description as Post, COUNT(likes.id) as Likes
FROM likes,posts
where posts.id = likes.post_id
group by likes.post_id
"""

with sqlite3.connect("sm_app.sqlite") as conn:
    user_headers,users = execute_read_query(conn, select_users)
    print(tabulate(users, headers=user_headers,tablefmt="fancy_grid"))

    post_headers,posts = execute_read_query(conn, select_posts)
    print(tabulate(posts, headers=post_headers,tablefmt="fancy_grid"))

    user_post_headers,users_posts = execute_read_query(conn, select_users_posts)
    print(tabulate(users_posts, headers=user_post_headers,tablefmt="fancy_grid"))

    post_comments_headers,posts_comments = execute_read_query(conn, select_posts_comments_users)
    print(tabulate(posts_comments, headers=post_comments_headers,tablefmt="fancy_grid"))

    post_likes_headers,posts_likes = execute_read_query(conn, select_post_likes)
    print(tabulate(posts_likes, headers=post_likes_headers,tablefmt="fancy_grid"))


