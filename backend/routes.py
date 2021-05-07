from flask import render_template, url_for, flash, redirect
from backend import app, db, bcrypt
from backend.forms import Registration_form, Login_form, Feedback_form
from backend.models import User, Book

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
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username = form.username.data, email = form.email.data, password = hashed_password, address = f'{form.street.data} {form.city.data} {form.state.data} {form.countries.data}')		
		db.session.add(user)		
		db.session.commit()
		flash("Your account has been created. You can now login!","success")
		return redirect(url_for("login"))
	return render_template('signup.html', title='Signup', form = form)
