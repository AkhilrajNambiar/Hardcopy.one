from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import Registration_form, Login_form, Feedback_form

app = Flask(__name__)
app.config['SECRET_KEY'] = '99d12359bfd5873cb57d85a1465f0f39'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(20), nullable=False)
	profile_pic = db.Column(db.String(60), nullable=False, default='default.jpg')	
	address = db.Column(db.Text, nullable=False)
	books_ordered = db.relationship('Book', backref='bought_by', lazy=True, foreign_keys='Book.ordered_by')
	books_donated = db.relationship('Book', backref='provided_by', lazy=True, foreign_keys='Book.donated_by')

	def __repr__(self):
		return f"User({self.username}, {self.email}, {self.profile_pic}, {self.address})"

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
		return f"Book({self.book_name}, {self.author_name}, {self.genre}, {self.donated_by}, {self.ordered_by})"


@app.route('/')
@app.route('/home')
def home():
	return render_template('index.html', title='Home')

@app.route('/about')
def about():
	return render_template('about.html', title='About')

@app.route('/contact', methods=['GET','POST'])
def contact():
	form = Feedback_form()
	if form.validate_on_submit():
		flash('Message successfully sent','success')
		return redirect(url_for('home'))
	return render_template('contact.html', title='Contact Me', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
	form = Login_form()
	if form.validate_on_submit():
		if form.email.data == 'admin@gmail.com' and form.password.data == 'Test':
			flash('You have successfully logged in!', category='success')
			return redirect(url_for('home'))
		else:
			flash('Wrong Email ID or Password!', category='danger')
	return render_template('login.html', title='Login', form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
	form = Registration_form()
	if form.validate_on_submit():
		flash("Your account has been registered. You can now login!","success")
		return redirect(url_for("login"))
	return render_template('signup.html', title='Signup', form = form)


if __name__ == '__main__':
	app.run(debug=True)