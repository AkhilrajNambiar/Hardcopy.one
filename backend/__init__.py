from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '99d12359bfd5873cb57d85a1465f0f39'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# The following statement is a prerequisite for the login_required decorator
login_manager.login_view = 'login'
login_manager.login_message_category = 'primary'

from backend import routes