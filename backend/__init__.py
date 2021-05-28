import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from backend.config import Config


# These are also known as extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
# The following statement is a prerequisite for the login_required decorator
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'primary'
mail = Mail()


# A function that creates the app
def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)


	#Adding these extensions with respect to a particular application
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app) 

	from backend.users.routes import users
	from backend.books.routes import books
	from backend.main.routes import main
	app.register_blueprint(users)
	app.register_blueprint(books)
	app.register_blueprint(main)

	return app