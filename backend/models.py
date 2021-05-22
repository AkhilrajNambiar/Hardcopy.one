from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from backend import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(50), nullable=False)
	profile_pic = db.Column(db.String(60), nullable=False, default='default.jpg')	
	address = db.Column(db.Text, nullable=False)
	books_ordered = db.relationship('Book', backref='bought_by', lazy=True, foreign_keys='Book.ordered_by')
	books_donated = db.relationship('Book', backref='provided_by', lazy=True, foreign_keys='Book.donated_by')
	carted = db.relationship('Cart', backref='added_by', lazy=True, foreign_keys='Cart.user_id')
	requested = db.relationship('PendingRequests', backref='requested_by', lazy=True, foreign_keys='PendingRequests.user_id')

	def get_reset_token(self, expires=1800):
		s = Serializer(app.config['SECRET_KEY'], expires)
		return s.dumps({'user_id':self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User({self.username}; {self.email}; {self.profile_pic}; {self.address})"

class Book(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	book_name = db.Column(db.String(60), nullable=False)
	author_name = db.Column(db.String(60), nullable=False)
	genre = db.Column(db.String(60), nullable=False)
	sub_genre = db.Column(db.String(60))
	book_front = db.Column(db.String(60), nullable=False, default='front.jpg')
	book_back = db.Column(db.String(60), nullable=False, default='back.jpg')
	book_top = db.Column(db.String(60), nullable=False, default='top.jpg')
	book_bottom = db.Column(db.String(60), nullable=False, default='back.jpg')
	book_right = db.Column(db.String(60), nullable=False, default='right.jpg')
	book_left = db.Column(db.String(60), nullable=False, default='left.jpg')
	extras = db.Column(db.Text)
	ordered_by = db.Column(db.Integer, db.ForeignKey('user.id'),default=0)
	donated_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	added_to_cart = db.relationship('Cart', backref='book_is', lazy=True, foreign_keys='Cart.book_id')
	

	def __repr__(self):
		return f"Book({self.book_name}; {self.author_name}; {self.genre}; {self.donated_by}; {self.ordered_by})"

class Cart(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=0)
	book_id = db.Column(db.Integer, db.ForeignKey('book.id'), default=0)

	def __repr__(self):
		return f"Cart({self.id}; {self.user_id}; {self.book_id})"

class PendingRequests(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	book_name = db.Column(db.String(60), nullable=False)
	author_name = db.Column(db.String(60), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=0)

	def __repr__(self):
		return f"Request({self.book_name}, {self.author_name}, {self.user_id})"
