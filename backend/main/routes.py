from flask import render_template, url_for, flash, redirect, Blueprint, current_app, request, abort, jsonify
from backend import db, mail
from backend.users.forms import Feedback_form, AddressUpdateForm
from backend.models import Book, User
from flask_login import current_user
import stripe
from flask_mail import Message
import json
import requests
import math
import random
import time

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('index.html', title='Home')


@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About')

@main.route('/donate', methods=['GET', 'POST'])
def donate():
    return render_template('donation.html', title='Donate')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = Feedback_form()
    if current_user.is_authenticated:
        form.name.data = current_user.username
        form.email.data = current_user.email
    if form.validate_on_submit():
        return render_template('contact_mail.html', title='Confirm sending', feedback=form.feedback.data, subject=form.subject.data)
    return render_template('contact.html', title='Contact Me', form=form)

def format_address(address):
    new_address = address.replace('#@',' ')
    return new_address

def place_order(book, user):
    auth = current_app.config['SHIPROCKET_TOKEN']
    url = "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"

    order_data = []

    my_order_id = f"{random.randint(100,999)}-{random.randint(100,999)}"

    address = user.address
    address_list = address.split('#@')
    country, pincode = address_list[3].split('-')

    payload = json.dumps({
      "order_id": f"{random.randint(100,999)}-{random.randint(100,999)}",
      "order_date": f'{time.localtime().tm_year}-{time.localtime().tm_mon if time.localtime().tm_mon >= 10 else f"0{time.localtime().tm_mon}"}-{time.localtime().tm_mday if time.localtime().tm_mday >= 10 else f"0{time.localtime().tm_mday}"}',
      "pickup_location": f"{book.provided_by.pickup}",
      "channel_id": "",
      "comment": "",
      "billing_customer_name": f"{user.username}",
      "billing_last_name": "",
      "billing_address": f"{address_list[0]}",
      "billing_address_2": "",
      "billing_city": f"{address_list[1]}",
      "billing_pincode": f"{pincode}",
      "billing_state": f"{address_list[2]}",
      "billing_country": f"{country}",
      "billing_email": f"{user.email}",
      "billing_phone": f"{user.contactnumber}",
      "shipping_is_billing": True,
      "shipping_customer_name": "",
      "shipping_last_name": "",
      "shipping_address": "",
      "shipping_address_2": "",
      "shipping_city": "",
      "shipping_pincode": "",
      "shipping_country": "",
      "shipping_state": "",
      "shipping_email": "",
      "shipping_phone": "",
      "order_items": [
        {
          "name": f"{book.book_name}",
          "sku": "",
          "units": 1,
          "selling_price": "0",
          "discount": "",
          "tax": "",
          "hsn": 0
        }
      ],
      "payment_method": "Prepaid",
      "shipping_charges": 0,
      "giftwrap_charges": 0,
      "transaction_charges": 0,
      "total_discount": 0,
      "sub_total": 0,
      "length": f"{book.length}",
      "breadth": f"{book.breadth}",
      "height": f"{book.height}",
      "weight": f"{(book.weight)/1000}"
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {auth}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    resjson = json.loads(response.text)
    order_data.append(resjson)
    print(order_data)
    return order_data

def Courier_check(order_id):
    import requests
    import json
    auth = current_app.config['SHIPROCKET_TOKEN']
    url = "https://apiv2.shiprocket.in/v1/external/courier/serviceability/"

    payload = json.dumps({
      # "pickup_postcode":"110006",
      # "delivery_postcode":"670141",
      # "weight":0.770,
      # "cod":False
      "order_id": f"{order_id}"
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {auth}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    parsed = json.loads(response.text)
    companies = parsed['data']['available_courier_companies']
    # print(json.dumps(companies, indent=4))
    rates = [i['rate'] for i in companies]
    minrate = min(rates)
    min_rate_company = []
    for i in companies:
      if i['rate'] == minrate:
        min_rate_company.append(i)
    return min_rate_company

def change_delivery_address(user, order_id, form):
    auth = current_app.config['SHIPROCKET_TOKEN']
    url = "https://apiv2.shiprocket.in/v1/external/orders/address/update"

    payload = json.dumps({
      "order_id": f"{order_id}",
      "shipping_customer_name": f"{user.username}",
      "shipping_phone": f"{user.contactnumber}",
      "shipping_address": f"{form.street.data}",
      "shipping_address_2": "",
      "shipping_city": f"{form.city.data}",
      "shipping_state": f"{form.state.data}",
      "shipping_country": f"{form.countries.data}",
      "shipping_pincode": f"{form.pincode.data}"
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {auth}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return f'{form.street.data}#@{form.city.data}#@{form.state.data}#@{form.countries.data}-{form.pincode.data}'

@main.route('/create-checkout-session/<int:book_id>/<int:user_id>', methods=['POST'])
def create_checkout_session(book_id,user_id):
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    if request.method == 'POST':
        book = Book.query.get(book_id)
        user = User.query.get(user_id)
        order_data = place_order(book, user)
        order_ka_id = order_data[0]['order_id']
        best_courier = Courier_check(order_ka_id)
        rate = best_courier[0]['rate']
        product1 = stripe.Product.create(
            name=book.book_name,
            images=[f'https://www.hardcopy.one/static/users_images/{book.book_front}'],
            description=f'By {book.author_name}'
        )
        price = stripe.Price.create(
            product=product1['id'],
            unit_amount= math.ceil(rate * 100) + 500,
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
            success_url=url_for('main.payment_success',user_id=user_id, book_id=book.id, shipment_id=order_data[0]['shipment_id'], courier_id=best_courier[0]['courier_company_id'], order_id=order_data[0]['order_id'], amount = rate+5, _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('main.payment_cancelled',user_id=user_id, book_id=book.id, _external=True)
        )
        form = AddressUpdateForm()
        display_address = format_address(current_user.address)
        if form.validate_on_submit():
            user = User.query.filter_by(username=current_user.username).first()
            addr = change_delivery_address(user, order_ka_id, form)
            display_address = format_address(addr)
    return render_template('orders.html', checkout_session_id=session['id'],
                           checkout_public_key=current_app.config['STRIPE_PUBLIC_KEY'], book=book, form=form, display_address = display_address)

def generate_awb(shipment_id, courier_id):
    auth = current_app.config['SHIPROCKET_TOKEN']
    url = "https://apiv2.shiprocket.in/v1/external/courier/assign/awb"
    payload = json.dumps({
      "shipment_id": f"{shipment_id}",
      "courier_id": f"{courier_id}"
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {auth}'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def shipment_pickup(shipment_id):
    auth = current_app.config['SHIPROCKET_TOKEN']
    url = "https://apiv2.shiprocket.in/v1/external/courier/generate/pickup"
    payload = json.dumps({
      "shipment_id": [
        shipment_id
      ]
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {auth}'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def generate_label(shipment_id):
    auth = current_app.config['SHIPROCKET_TOKEN']
    url = "https://apiv2.shiprocket.in/v1/external/courier/generate/label"
    payload = json.dumps({
      "shipment_id": [
        shipment_id
      ]
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {auth}'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def shipment_kaisa_hai(shipment_id):
    auth = current_app.config['SHIPROCKET_TOKEN']
    url = f"https://apiv2.shiprocket.in/v1/external/courier/track/shipment/{shipment_id}"
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {auth}'
    }

    response = requests.request("GET", url, headers=headers)

    track = json.loads(response.text)
    # print(track)
    # print(track['tracking_data']['track_url'])
    try:
        return track['tracking_data']['shipment_track'][0]['current_status']
    except:
        return 'Untracked'

@main.route('/payment_success/<int:book_id>/<int:user_id>/<shipment_id>/<courier_id>/<order_id>/<amount>')
def payment_success(book_id, user_id, shipment_id, courier_id, order_id, amount):
    user = User.query.filter_by(id=user_id).first()
    book = Book.query.filter_by(id=book_id).first()
    donor = User.query.filter_by(id=book.donated_by).first()
    generate_awb(shipment_id, courier_id)
    shipment_pickup(shipment_id)
    generate_label(shipment_id)
    book.ordered_by = user_id
    book.shipment_id = str(shipment_id)
    book.shipment_status = shipment_kaisa_hai(shipment_id)
    book.order_id = str(order_id)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    samay = f"{months[int(time.localtime().tm_mon - 1)]}, {time.localtime().tm_mday} {time.localtime().tm_year}  {time.localtime().tm_hour}:{time.localtime().tm_min}"
    book.order_date = samay
    db.session.commit()
    msg = Message('A new order', sender='noreply@demo.com',recipients=['nambiarakhilraj01@gmail.com'])
    msg.html = f"""
    <h1>A new order was made</h1>
    <h3>Ordered by: {user.username}</h3>
    <h3>Book name: {book.book_name}</h3>
    """
    mail.send(msg)
    newmsg = Message('Receipt for your order', sender='noreply@demo.com', recipients=[f'{user.email}'])
    newmsg.html = f"""
    <div class="container">
        <div class="row" style="background-color:black;">
            <br><br>
            <div class="col-12">
                <center><img src="{{url_for('static', filename='admin_images/logo2small.webp')}}" width="120" height="156" alt="hardcopy_logo"></center>
            </div>
            <div class="col-12 text-center" style="color: white;font-family:calibri;" >
                <center><h2>Receipt for Scion of Ikshvaku</h2></center>
            </div>
        </div>
        <div class="row">
            <div class="col-12 text-center" style="font-family:calibri;">
                <center><h3>SUMMARY</h3></center>
            </div>
        </div>
        <div class="row" style="font-family:calibri;">
            <center><h3><b style="color:orange;">Book Name</b> : {book.book_name}</h3></center>
        </div>
        <div class="row" style="font-family:calibri;">
            <center><h3><b style="color:orange;">Amount paid</b> : &#8377;{amount}</h3></center>
        </div>
        <div class="row" style="font-family:calibri;">
            <center><h3><b style="color:orange;">Bought by</b> : {user.username}</h3></center>
        </div>
        <div class="row" style="font-family:calibri;">
            <center><h3><b style="color:orange;">Donated by</b> : {donor.username}</h3></center>
        </div>
    </div>
    """
    # mail.send(newmsg)
    return render_template('payment_success.html', book=book)

@main.route('/tracking/<shipment_id>')
def tracking(shipment_id):
    auth = current_app.config['SHIPROCKET_TOKEN']
    url = f"https://apiv2.shiprocket.in/v1/external/courier/track/shipment/{shipment_id}"
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {auth}'
    }

    response = requests.request("GET", url, headers=headers)

    track = json.loads(response.text)
    try:
        tracking_url = track['tracking_data']['track_url']
        return redirect(tracking_url)
    except:
        return render_template('not_tracked.html')

@main.route('/payment_cancelled/<int:user_id>')
def payment_cancelled(user_id):
    return render_template('payment_cancelled.html')

@main.route('/stripe_webhook', methods=['POST'])    
def stripe_webhook():
    print('WEBHOOK CALLED')
    event = None

    payload = request.data

    try:

        event = json.loads(payload)

    except Exception as e:

        print(' Webhook error while parsing basic request.' + str(e))

        return jsonify(success=False)

    # Handle the event
    charge_event = {}
    if event and event['type'] == 'payment_intent.succeeded':

        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent

        print('Payment for {} succeeded'.format(payment_intent['amount']))

        # Then define and call a method to handle the successful payment intent.
        payment_king = json.dumps(payment_intent, indent=2)
        print(payment_king)

    elif event['type'] == 'payment_method.attached':

        payment_method = event['data']['object']  # contains a stripe.PaymentMethod

        # Then define and call a method to handle the successful attachment of a PaymentMethod.

        # handle_payment_method_attached(payment_method)
        print(payment_method)

    elif event['type'] == 'charge.succeeded':

        charges = json.dumps(event, indent=2)
        print(charges)
        charge_event = event['data']['object']
        msg = Message('Receipt for your order!', sender='noreply@demo.com',recipients=[charge_event['billing_details']['email']])
        receipt = requests.get(charge_event['receipt_url'])
        msg.html = receipt.content
        mail.send(msg)

    elif event['type'] == 'checkout.session.completed':

        success = json.dumps(event, indent=2)
        print(success)
        

    else:

        # Unexpected event type

        print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)

@main.route('/invoice/<string:order_id>', methods=['POST','GET'])
def generate_invoice(order_id):
    auth = current_app.config['SHIPROCKET_TOKEN']
    url = "https://apiv2.shiprocket.in/v1/external/orders/print/invoice"
    payload = json.dumps({
      "ids": [
        f"{order_id}"
      ]
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {auth}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    data = json.loads(response.text)
    print(data)
    try:
        return redirect(data['invoice_url'])
    except:
        return "There is an error"

@main.route('/cancel_order/<string:order_id>')
def cancel_order(order_id):
    auth = current_app.config['SHIPROCKET_TOKEN']
    url = "https://apiv2.shiprocket.in/v1/external/orders/cancel"
    payload = json.dumps({
      "ids": [
        f"{order_id}"
      ]
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {auth}'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    book = Book.query.filter_by(order_id=order_id).first()
    order_karne_waala = User.query.get(book.ordered_by)
    msg = Message('Order cancellation', sender='noreply@demo.com', recipients=['nambiarakhilraj01@gmail.com'])
    msg.html = f"""
    <h1>Order for {book.book_name} has been cancelled</h1>
    <h2>Ordered by {order_karne_waala.username}!</h2>
    <h3>Ordered data is approx {book.order_date}</h3>
    <h3>Refund this order through stripe!!</h3>
    """
    mail.send(msg)
    book.ordered_by = None
    db.session.commit()
    flash('Your order was successfully cancelled', 'success')
    return redirect(url_for('main.home'))
