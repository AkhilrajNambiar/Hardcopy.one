from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from backend import db, bcrypt
from backend.users.forms import Registration_form, Login_form, Update_form, \
    RequestResetForm, ResetPasswordForm
from backend.models import User, Book, Cart
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import and_
from backend.users.utils import send_reset_email, save_picture
import requests
import random
import json
from backend.main.routes import shipment_kaisa_hai

users = Blueprint('users', __name__)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = Login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                flash(f'Welcome back, {user.username}!!', 'success')
                return redirect(next_page)
            flash(f'Welcome back, {user.username}!!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Wrong Email ID or Password!', category='danger')
    return render_template('login.html', title='Login', form=form)

def add_pickup_address(user):
    auth = current_app.config['SHIPROCKET_TOKEN']
    url = "https://apiv2.shiprocket.in/v1/external/settings/company/addpickup"
    address = user.address
    address_list = address.split('#@')
    country, pincode = address_list[3].split('-') 
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']   
    pickup = ''
    for i in range(7):
        pickup += alphabet[random.randint(0,25)]   

    payload = json.dumps({
      "pickup_location": pickup,
      "name": f"{user.username}",
      "email": f"{user.email}",
      "phone": f"{user.contactnumber}",
      "address": f"{address_list[0]}",
      "address_2": "",
      "city": f"{address_list[1]}",
      "state": f"{address_list[2]}",
      "country": f"{country}",
      "pin_code": f"{pincode}"
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {auth}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)   
    return pickup

@users.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Registration_form()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    address=f'{form.street.data}#@{form.city.data}#@{form.state.data}#@{form.countries.data}-{form.pincode.data}', contactnumber=form.contactnumber.data)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(username=form.username.data).first()
        pickup = add_pickup_address(user)
        user.pickup = pickup
        db.session.commit()
        flash("Your account has been created. You can now login!", "success")
        return redirect(url_for("users.login"))
    return render_template('signup.html', title='Signup', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/cart/<user_id>')
@login_required
def cart(user_id):
    if current_user.is_authenticated:
        return render_template('cart.html', title=f'{current_user.username}s cart')

@users.route('/orders/<user_id>')
@login_required
def orders(user_id):
    if current_user.is_authenticated:
        bookall = Book.query.all()
        books = []
        for book in bookall:
            if int(user_id) == book.ordered_by:
                book.shipment_status = shipment_kaisa_hai(book.shipment_id)
                db.session.commit()
                books.append(book)
        return render_template('user_orders.html', books=books, user_id=user_id)

@users.route('/add_to_cart', methods=['GET', 'POST'])
@login_required
def add_to_cart_for_no_user():
    if not current_user.is_authenticated:
        flash('Please login to view this page', 'primary')
        return redirect(url_for('users.login'))
    return redirect(url_for('users.add_to_cart', user_id = current_user.id))


@users.route('/add_to_cart/<user_id>', methods=['GET', 'POST'])
@login_required
def add_to_cart(user_id):
    if request.method == 'POST':
        if 'cartbtn' in request.form:
            book_id = request.form['cartbtn']
            cart = Cart(user_id=user_id, book_id=book_id)
            db.session.add(cart)
            db.session.commit()
        flash('Book successfully added to cart', 'success')
    user_cart = Cart.query.filter_by(user_id=current_user.id)
    book_list = []
    for cart in user_cart:
        book_list.append(cart.book_is)
    return render_template('cart.html', books=book_list)


@users.route('/remove_from_cart/<user_id>', methods=['GET', 'POST'])
@login_required
def remove_from_cart(user_id):
    if request.method == 'POST':
        if 'cartremovebtn' in request.form:
            book_id = request.form['cartremovebtn']
            book_in_cart = Cart.query.filter(and_(Cart.user_id == current_user.id, Cart.book_id == book_id))
            book_to_remove = book_in_cart[0]
            db.session.delete(book_to_remove)
            db.session.commit()
        flash('Book successfully removed from cart', 'success')
        return redirect(url_for('users.add_to_cart', user_id=current_user.id))


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    # we have to log out the user while they reset their password
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset password', 'primary')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token!', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Your password was successfully reset!", "success")
        return redirect(url_for("users.login"))
    return render_template('reset_password.html', title='Reset Password', form=form)

@users.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'users_images/{current_user.profile_pic}')
    books = Book.query.filter_by(donated_by=current_user.id)
    return render_template('account.html', title="User Account", image_file=image_file, form=form, books=books)

