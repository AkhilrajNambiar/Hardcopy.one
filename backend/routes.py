from flask import render_template, url_for, flash, redirect, request
from backend import app, db, bcrypt
from backend.forms import Registration_form, Login_form, Feedback_form
from backend.models import User, Book
from flask_login import login_user, current_user, logout_user, login_required

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
	if current_user.is_authenticated:
            form.name.data = current_user.username
            form.email.data = current_user.email
	if form.validate_on_submit():
		flash('Message successfully sent','success')
		return redirect(url_for('home'))
	return render_template('contact.html', title='Contact Me', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
	form = Login_form()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			if next_page:
				flash(f'Welcome back, {user.username}!!','success')
				return redirect(next_page)
			flash(f'Welcome back, {user.username}!!','success')
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

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
	return render_template('account.html', title="User Account")