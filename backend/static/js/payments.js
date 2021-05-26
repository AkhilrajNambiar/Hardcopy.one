var stripe = Stripe(checkout_public_key);
const button = document.querySelector('#checkout-button');
button.addEventListener('click', event => {
	stripe.redirectToCheckout({
		sessionId: checkout_session_id
	}).then(function(result){

	});
});