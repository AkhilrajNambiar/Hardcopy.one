from flask import Flask, render_template, url_for
from forms import Registration_form

app = Flask(__name__)
app.config['SECRET_KEY'] = '99d12359bfd5873cb57d85a1465f0f39'

@app.route('/')
@app.route('/home')
def home():
	return render_template('index.html', title='Home')

@app.route('/about')
def about():
	return render_template('about.html', title='About')

@app.route('/contact')
def contact():
	return render_template('contact.html', title='Contact Me')

@app.route('/login')
def login():
	return render_template('login.html', title='Login')

@app.route('/signup')
def signup():
	form = Registration_form()
	return render_template('signup.html', title='Signup', form = form)


if __name__ == '__main__':
	app.run(debug=True)