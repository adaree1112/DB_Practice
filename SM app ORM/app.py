from typing import Optional
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import User, Post, Comment
import pyinputplus as pyip

class Controller:
    def __init__(self,db_location='sqlite:///Sm_app.sqlite'):
        self.current_user = None
        self.engine = create_engine(db_location)

    def set_current_user_from_name(self, name):
        with Session(bind=self.engine) as session:
            self.current_user = session.scalars(select(User).where(User.name == name)).one_or_none()

    def get_user_names(self) -> list[str]:
        with Session(bind=self.engine) as session:
            user_names = session.scalars(select(User.name).order_by(User.name)).all()
        return list(user_names)

    def create_user(self, name: str, age: int, gender: str, nationality: str) -> User:
        with Session(bind=self.engine) as session:
            user= User(name=name, age=age, gender=gender, nationality=nationality)
            user = session.merge(user)
            session.add(user)
            session.commit()
            session.refresh(user)
            self.current_user = user
        return user

    def create_post(self, title, description) -> Post:
        user=self.current_user
        with Session(bind=self.engine) as session:
            user = session.merge(user)
            post= Post(title=title,description=description,)
            user.posts.append(post)
            session.commit()
            session.refresh(post)
            self.current_user = user
            return post

    def get_current_user(self):
        with Session(bind=self.engine) as session:
            if self.current_user is not None:
                return session.merge(self.current_user)
            else:
                return None

    def get_posts(self, user_name: str) -> list[dict]:
        with Session(bind=self.engine) as session:
            user = session.scalars(select(User).where(User.name == user_name)).one_or_none()
            posts_info = []
            if user:
                for post in user.posts:
                    comments_info = [{"user": comment.user.name, "comment": comment.comment} for comment in
                                     post.comments]
                    posts_info.append({
                        "id": post.id,
                        "title": post.title,
                        "description": post.description,
                        "number_likes": len(post.liked_by_user),
                        "comments": comments_info
                    })
        return posts_info

    def add_comment(self, post_id: int, comment_text: str):
        user = self.get_current_user()
        with Session(bind=self.engine) as session:
            user = session.merge(user)
            post = session.get(Post, post_id)
            if post:
                comment = Comment(user=user, post=post, comment=comment_text)
                session.add(comment)
                session.commit()

    def like_post(self, post_id: int):
        user = self.get_current_user()
        with Session(bind=self.engine) as session:
            user = session.merge(user)
            post = session.get(Post, post_id)
            if post:  # added if post exists
                if user in post.liked_by_user:
                    post.liked_by_user.remove(user)
                else:
                    post.liked_by_user.append(user)
                session.commit()

class CLI:
    def __init__(self):
        self.controller = Controller()
        self.login()

    @staticmethod
    def show_title(title):
        print("\n"+title)
        print("-"*len(title)+"\n")

    def login(self):
        self.show_title("Login Screen")
        users=self.controller.get_user_names()
        menu_items = users + ['Create a new account'] + (
            ['Create a new post'] if self.controller.current_user is not None else []) + ['Exit']
        menu_choice = pyip.inputMenu(menu_items, prompt='Select a user or create a new account\n', numbered=True)

        if menu_choice == 'Create a new account':
            self.create_account()
        elif menu_choice == 'Create a new post':
            self.create_post()
        elif menu_choice == 'Exit':
            print("Goodbye")
        else:
            user_name=menu_choice
            self.controller.set_current_user_from_name(user_name)
            self.user_home()

    def create_account(self, existing_users = None):
        self.show_title("Create Account Screen")
        print("Enter Account Details")

        user_name=pyip.inputStr(prompt="Username: ", blockRegexes=existing_users, strip=None)
        age=pyip.inputInt(prompt="Age: ", min=13, max=120, blank=True)
        gender= pyip.inputMenu(["Male", "Female","Other"], prompt="Gender: ", numbered=True, blank=True)
        nationality = pyip.inputStr(prompt="Nationality: ")

        self.controller.create_user(user_name, age, gender, nationality)
        self.login()

    def create_post(self):
        self.show_title("Create Post Screen")
        print("Enter Post Details")

        title=pyip.inputStr(prompt="Title: ", strip=None)
        description=pyip.inputStr(prompt="Description: ", strip=None)

        self.controller.create_post(title, description)


    def user_home(self):
        current_user = self.controller.get_current_user()
        self.show_title(f"{current_user.name} Home Screen")
        print(f"Name: {current_user.name}")
        print(f"Age: {current_user.age}")
        print(f"Nationality: {current_user.nationality}")

        self.show_posts(current_user.name)

        menu_items = {'Show posts from another user': self.show_posts,
                      'Create a new post': self.create_post,
                      'Logout': self.login, }

        menu_keys = list(menu_items.keys())

        menu_choice = pyip.inputMenu(menu_keys, prompt='Select an action\n', numbered=True)

        menu_items[menu_choice]()

        if menu_choice != "Logout":
            self.user_home()

    def show_posts(self, user_name: Optional[str] = None):
        if user_name is None:
            users = self.controller.get_user_names()
            menu_choice = pyip.inputMenu(users, prompt='Select a user', numbered=True)
            user_name = menu_choice

        self.show_title(f"{user_name} Posts Screen")
        posts = self.controller.get_posts(user_name)
        for post in posts:
            print(f"Title: {post['title']}")
            print(f"Content: {post['description']}")
            print(f"Likes: {post['number_likes']}")
            for comment in post['comments']:
                print(f"  {comment['user']}: {comment['comment']}")

            actions = ['Like', 'Comment']
            action = pyip.inputMenu(actions, prompt='Select an action (or press Enter to skip):', numbered=True,
                                    blank=True)

            if action == 'Like':
                self.controller.like_post(post['id'])
            elif action == 'Comment':
                comment_text = pyip.inputStr(prompt='Enter your comment: ')
                self.controller.add_comment(post['id'], comment_text)

        if not posts:
            print("No posts found")
if __name__=="__main__":
    CLI()
