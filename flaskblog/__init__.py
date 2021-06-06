from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '5280d1b679888c1a9de74708f3eb1971'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # configuration
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # we need to tell the login_manager the route for login
login_manager.login_message_category = 'info'   # setting the bootstrap class for message logged in



from flaskblog import routes



