from flask import render_template, url_for, flash, redirect, Blueprint, current_app
from backend import db, mail
from backend.users.forms import Feedback_form, AddressUpdateForm
from backend.models import Book, User
from flask_login import current_user
import webbrowser
import stripe
from flask_mail import Message

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('index.html', title='Home')


@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About')


@main.route('/contact', methods=['GET', 'POST'])
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
        return redirect(url_for('main.home'))
    return render_template('contact.html', title='Contact Me', form=form)



@main.route('/create-checkout-session/<int:book_id>/<int:user_id>', methods=['POST'])
def create_checkout_session(book_id,user_id):
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
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
        success_url=url_for('main.payment_success',user_id=user_id, book_id=book.id, _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('main.payment_cancelled',user_id=user_id, book_id=book.id, _external=True)
    )
    form = AddressUpdateForm()
    if form.validate_on_submit():
        current_user.address = f'{form.street.data} {form.city.data} {form.state.data} {form.countries.data}'
        db.session.commit()
    return render_template('orders.html', checkout_session_id=session['id'],
                           checkout_public_key=current_app.config['STRIPE_PUBLIC_KEY'], book=book, form=form)


@main.route('/payment_success/<int:book_id>/<int:user_id>')
def payment_success(book_id, user_id):
    user = User.query.filter_by(id=user_id).first()
    book = Book.query.filter_by(id=book_id).first()
    donor = User.query.filter_by(id=book.donated_by).first()

    msg = Message('Receipt for your book', sender='noreply@demo.com', recipients=[user.email])
    msg.html = f'''
<p>Hello {user.username}, this is the receipt for {book.book_name}:</p>
                    
<center>
<h1>{ book.book_name }</h1>
<br>
<strong>Author</strong> : { book.author_name }
<br>
<strong>Amount Paid</strong> : 40 Rs.
<br>
<strong>Donor email</strong> : {donor.email}
<br>
<strong>Delivery Address Address</strong> : {user.address}
<br><br>
<p>Thank you for using Hardcopy.com, and happy reading!</p>
</center>
'''
    mail.send(msg)
    return render_template('payment_success.html')


@main.route('/payment_cancelled/<int:user_id>')
def payment_cancelled(user_id):
    return render_template('payment_cancelled.html')