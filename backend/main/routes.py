from flask import render_template, url_for, flash, redirect, Blueprint, current_app
from backend import db
from backend.users.forms import Feedback_form, AddressUpdateForm
from backend.models import Book
from flask_login import current_user
import webbrowser
import stripe

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



@main.route('/create-checkout-session/<int:book_id>', methods=['POST'])
def create_checkout_session(book_id):
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
        success_url=url_for('main.payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('main.payment_cancelled', _external=True)
    )
    form = AddressUpdateForm()
    if form.validate_on_submit():
        current_user.address = f'{form.street.data} {form.city.data} {form.state.data} {form.countries.data}'
        db.session.commit()
    return render_template('orders.html', checkout_session_id=session['id'],
                           checkout_public_key=current_app.config['STRIPE_PUBLIC_KEY'], book=book, form=form)


@main.route('/payment_success')
def payment_success():
    return render_template('payment_success.html')


@main.route('/payment_cancelled')
def payment_cancelled():
    return render_template('payment_cancelled.html')