import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from backend.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# The following statement is a prerequisite for the login_required decorator
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'primary'
mail = Mail(app)

from backend.users.routes import users
from backend.books.routes import books
from backend.main.routes import main

app.register_blueprint(users)
app.register_blueprint(books)
app.register_blueprint(main)
