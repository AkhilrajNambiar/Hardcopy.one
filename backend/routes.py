import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from backend import app, db, bcrypt
from backend.forms import Registration_form, Login_form, Feedback_form, Update_form, BookUploadForm
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

# This method is simply responsible for saving the user's picture to our system
def save_picture(form_picture):
	# Giving a random name to the file to avoid naming conflicts with other files
	random_hex = secrets.token_hex(16)
	# Getting the extension of the file that the user has uploaded
	_,f_ext = os.path.splitext(form_picture.filename)
	# Giving the picture the random name but conserving the same extension that the user had uploaded
	picture_fn = random_hex + f_ext
	# Setting the path where the user pictures will be stored
	picture_path = os.path.join(app.root_path, 'static/users_images', picture_fn)

	# This is to resize the image
	dimensions = (125,125)	
	i = Image.open(form_picture)
	i.thumbnail(dimensions)

	# Saving the picture with the random name to the created path	
	i.save(picture_path)

	return picture_fn	

def save_picture_without_compression(form_picture):
	# Giving a random name to the file to avoid naming conflicts with other files
	random_hex = secrets.token_hex(16)
	# Getting the extension of the file that the user has uploaded
	_,f_ext = os.path.splitext(form_picture.filename)
	# Giving the picture the random name but conserving the same extension that the user had uploaded
	picture_fn = random_hex + f_ext
	# Setting the path where the user pictures will be stored
	picture_path = os.path.join(app.root_path, 'static/users_images', picture_fn)

	# Saving the picture with the random name to the created path	
	form_picture.save(picture_path)

	return picture_fn	


@app.route('/account', methods=['GET','POST'])
@login_required
def account():
	form = Update_form()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.profile_pic = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account was successfully updated', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename=f'users_images/{current_user.profile_pic}')
	return render_template('account.html', title="User Account", image_file=image_file, form=form)

@app.route('/upload', methods=['GET','POST'])
@login_required	
def upload():
	form = BookUploadForm()
	if form.validate_on_submit():
		book = Book(book_name=form.book_name.data, author_name=form.author_name.data, genre=form.genre.data, book_front=save_picture_without_compression(form.book_front.data), book_back=save_picture_without_compression(form.book_back.data), book_top=save_picture_without_compression(form.book_top.data), book_bottom=save_picture_without_compression(form.book_bottom.data), book_right=save_picture_without_compression(form.book_right.data), book_left=save_picture_without_compression(form.book_left.data), provided_by=current_user)
		db.session.add(book)				
		db.session.commit()
		flash("Book has been successfully uploaded. Thank you for your contribution!","success")
		return redirect(url_for('home'))		
	return render_template('upload.html', title="Upload Books here", form=form)