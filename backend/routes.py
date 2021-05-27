import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, jsonify
from backend import app, db, bcrypt, mail
from backend.forms import Registration_form, Login_form, Feedback_form, Update_form, BookUploadForm, BookRequestForm, \
    RequestResetForm, ResetPasswordForm, AddressUpdateForm
from backend.models import User, Book, Cart, PendingRequests
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import or_, and_
import webbrowser
from flask_mail import Message
import stripe


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('index.html', title='Home')


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = Feedback_form()
    if current_user.is_authenticated:
        form.name.data = current_user.username
        form.email.data = current_user.email
    if form.validate_on_submit():
        webbrowser.open(f"mailto:nambiarakhilraj01@gmail.com?subject={form.subject.data}&body={form.feedback.data}", autoraise=True)
        # msg = Message(form.subject.data, sender=form.email.data, recipients=['nambiarakhilraj01@gmail.com'])
        # msg.body = form.feedback.data
        # mail.send(msg)
        flash('Message successfully added to mail client', 'success')
        return redirect(url_for('home'))
    return render_template('contact.html', title='Contact Me', form=form)


@app.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('home'))
        else:
            flash('Wrong Email ID or Password!', category='danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Registration_form()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    address=f'{form.street.data} {form.city.data} {form.state.data} {form.countries.data}')
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created. You can now login!", "success")
        return redirect(url_for("login"))
    return render_template('signup.html', title='Signup', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# This method is simply responsible for saving the user's picture to our system
def save_picture(form_picture):
    # Giving a random name to the file to avoid naming conflicts with other files
    random_hex = secrets.token_hex(16)
    # Getting the extension of the file that the user has uploaded
    _, f_ext = os.path.splitext(form_picture.filename)
    # Giving the picture the random name but conserving the same extension that the user had uploaded
    picture_fn = random_hex + f_ext
    # Setting the path where the user pictures will be stored
    picture_path = os.path.join(app.root_path, 'static/users_images', picture_fn)

    # This is to resize the image
    dimensions = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(dimensions)

    # Saving the picture with the random name to the created path
    i.save(picture_path)

    return picture_fn


def save_picture_without_compression(form_picture):
    # Giving a random name to the file to avoid naming conflicts with other files
    random_hex = secrets.token_hex(16)
    # Getting the extension of the file that the user has uploaded
    _, f_ext = os.path.splitext(form_picture.filename)
    # Giving the picture the random name but conserving the same extension that the user had uploaded
    picture_fn = random_hex + f_ext
    # Setting the path where the user pictures will be stored
    picture_path = os.path.join(app.root_path, 'static/users_images', picture_fn)

    # Saving the picture with the random name to the created path
    form_picture.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
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
    books = Book.query.filter_by(donated_by=current_user.id)
    return render_template('account.html', title="User Account", image_file=image_file, form=form, books=books)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = BookUploadForm()
    if form.validate_on_submit():
        pending = PendingRequests.query.all()
        pending_books = []
        for book in pending:
            pending_books.append(book.book_name)
        if form.book_name.data in pending_books:
            uploaded_book = PendingRequests.query.filter_by(book_name=form.book_name.data)
            db.session.delete(uploaded_book[0])
            db.session.commit()
        book = Book(book_name=form.book_name.data, author_name=form.author_name.data, genre=form.genre.data,
                    sub_genre=form.sub_genre.data, book_front=save_picture_without_compression(form.book_front.data),
                    book_back=save_picture_without_compression(form.book_back.data),
                    book_top=save_picture_without_compression(form.book_top.data),
                    book_bottom=save_picture_without_compression(form.book_bottom.data),
                    book_right=save_picture_without_compression(form.book_right.data),
                    book_left=save_picture_without_compression(form.book_left.data), provided_by=current_user)
        db.session.add(book)
        db.session.commit()
        flash("Book has been successfully uploaded. Thank you for your contribution!", "success")
        return redirect(url_for('home'))
    return render_template('upload.html', title="Upload Books here", form=form)


@app.route('/fiction', methods=['GET', 'POST'])
def fiction():
    books = Book.query.all()
    return render_template('fiction.html', title='Fiction', books=books)


@app.route('/non_fiction', methods=['GET', 'POST'])
def non_fiction():
    books = Book.query.all()
    return render_template('non-fiction.html', title='Non-fiction', books=books)


@app.route('/biography', methods=['GET', 'POST'])
def biography():
    books = Book.query.all()
    return render_template('biography.html', title='Biography', books=books)


@app.route('/comics', methods=['GET', 'POST'])
def comics():
    books = Book.query.all()
    return render_template('comics.html', title='Comics', books=books)


@app.route('/romance', methods=['GET', 'POST'])
def romance():
    books = Book.query.all()
    return render_template('romance.html', title='Romance', books=books)


@app.route('/personality', methods=['GET', 'POST'])
def personality():
    books = Book.query.all()
    return render_template('personality.html', title='Self-Help', books=books)


@app.route('/book_page/<int:book_id>', methods=['GET', 'POST'])
def book_page(book_id):
    book = Book.query.get_or_404(book_id)
    other_books_by_author = Book.query.filter_by(author_name=book.author_name)
    in_the_cart = False
    if current_user.is_authenticated:
        hai_ya_nahi = Cart.query.filter(and_(Cart.user_id == current_user.id, Cart.book_id == book_id))
        if hai_ya_nahi.count() == 1:
            in_the_cart = True
    return render_template('book_page.html', title=book.book_name, book=book,
                           other_books_by_author=other_books_by_author, in_the_cart=in_the_cart)


def book_search(query):
    matched_books = []
    query = query.capitalize()
    book_list = Book.query.all()
    for i in book_list:
        if query in i.book_name or query in i.genre or query in i.author_name or query in i.sub_genre:
            matched_books.append(i)
    return matched_books


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('searchbar')
    matched_books = book_search(query)
    return render_template('search_results.html', title=f'Search result for {query}', matched_books=matched_books,
                           query=query)


@app.route('/cart/<user_id>')
@login_required
def cart(user_id):
    if current_user.is_authenticated:
        return render_template('cart.html', title=f'{current_user.username}s cart')


@app.route('/add_to_cart', methods=['GET', 'POST'])
@login_required
def add_to_cart_for_no_user():
    if not current_user.is_authenticated:
        flash('Please login to view this page', 'primary')
        return redirect(url_for('login'))
    return redirect(url_for('add_to_cart', user_id = current_user.id))


@app.route('/add_to_cart/<user_id>', methods=['GET', 'POST'])
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


@app.route('/remove_from_cart/<user_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('add_to_cart', user_id=current_user.id))


# pending_requests = []
@app.route('/request_book', methods=['GET', 'POST'])
@login_required
def request_book():
    form = BookRequestForm()
    if form.validate_on_submit():
        books = Book.query.all()
        book_names = []
        # global pending_requests
        for book in books:
            book_names.append(book.book_name)
        if form.book_name.data not in book_names:
            pending_requests = PendingRequests(book_name=form.book_name.data, author_name=form.author_name.data,
                                               user_id=current_user.id)
            db.session.add(pending_requests)
            db.session.commit()
            flash('Request successfully posted!', 'success')
            return redirect(url_for('request_book'))
        else:
            flash('The book already exists in our website. Please check!', 'danger')
    return render_template('request.html', title='Community', form=form, pending_requests=PendingRequests.query.all())


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f"""To reset the password go to following link:
{url_for('reset_password', token=token, _external=True)}
If you did not make this request, please ignore this message and there won't be any changes made!
"""
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    # we have to log out the user while they reset their password
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset password', 'primary')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token!', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Your password was successfully reset!", "success")
        return redirect(url_for("login"))
    return render_template('reset_password.html', title='Reset Password', form=form)


stripe.api_key = app.config['STRIPE_SECRET_KEY']


@app.route('/create-checkout-session/<int:book_id>', methods=['POST'])
def create_checkout_session(book_id):
    book = Book.query.get(book_id)
    product1 = stripe.Product.create(
        name=book.book_name,
        # images=['file:///C:/Hardcopy_old/images/book_front.jpg']
        description=f'By {book.author_name}'
    )
    price = stripe.Price.create(
        product=product1['id'],
        unit_amount=4000,
        currency='inr'
    )
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price': price['id'],
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=url_for('payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('payment_cancelled', _external=True)
    )
    form = AddressUpdateForm()
    if form.validate_on_submit():
        current_user.address = f'{form.street.data} {form.city.data} {form.state.data} {form.countries.data}'
        db.session.commit()
    return render_template('orders.html', checkout_session_id=session['id'],
                           checkout_public_key=app.config['STRIPE_PUBLIC_KEY'], book=book, form=form)


@app.route('/payment_success')
def payment_success():
    return render_template('payment_success.html')


@app.route('/payment_cancelled')
def payment_cancelled():
    return render_template('payment_cancelled.html')
