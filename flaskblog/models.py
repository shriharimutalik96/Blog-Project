from flaskblog import db,login_manager
from datetime import datetime
from flask_login import UserMixin        # conatins 4 methods to check the whather the user is autheticated or not


# this is crated in-order to maintain the session of the user
# reloading the user from the user-id stored in the session
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


class User(db.Model,UserMixin):

  # Creating User class for every user :

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
  password = db.Column(db.String(120), nullable=False)
  posts = db.relationship('Post',backref='author',lazy=True)

  # This filed is a list of the all posts created by the specified User
  # one to many relationship : One user can have a multiple posts
  # but a post will have single user

  def __repr__(self):

    return f"User('{self.username}','{self.email}','{self.image_file}')"






# Each class will be table on the database
class Post(db.Model):

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200),nullable=False)
  date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
  content = db.Column(db.Text,nullable=False)
  user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
  # author is a child of user , so we have used ForeignKey
  # author_id is coming from user_id , here USER is parent and author is child

  def __repr__(self):
    return f"Post('{self.author_id}','{self.title}' ,'{self.date_posted}')"
