from backend import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(20), nullable=False)
	profile_pic = db.Column(db.String(60), nullable=False, default='default.jpg')	
	address = db.Column(db.Text, nullable=False)
	books_ordered = db.relationship('Book', backref='bought_by', lazy=True, foreign_keys='Book.ordered_by')
	books_donated = db.relationship('Book', backref='provided_by', lazy=True, foreign_keys='Book.donated_by')

	def __repr__(self):
		return f"User({self.username}; {self.email}; {self.profile_pic}; {self.address})"

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	book_name = db.Column(db.String(20), nullable=False)
	author_name = db.Column(db.String(20), nullable=False)
	genre = db.Column(db.String(60), nullable=False)
	book_front = db.Column(db.String(60), nullable=False, default='front.jpg')
	book_back = db.Column(db.String(60), nullable=False, default='back.jpg')
	book_top = db.Column(db.String(60), nullable=False, default='top.jpg')
	book_bottom = db.Column(db.String(60), nullable=False, default='back.jpg')
	book_right = db.Column(db.String(60), nullable=False, default='right.jpg')
	book_left = db.Column(db.String(60), nullable=False, default='left.jpg')
	ordered_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	donated_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	

	def __repr__(self):
		return f"Book({self.book_name}; {self.author_name}; {self.genre}; {self.donated_by}; {self.ordered_by})"
