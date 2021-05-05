from flask import Flask, render_template, url_for, flash, redirect
from forms import Registration_form, Login_form, Feedback_form

app = Flask(__name__)
app.config['SECRET_KEY'] = '99d12359bfd5873cb57d85a1465f0f39'

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
	return render_template('contact.html', title='Contact Me', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
	form = Login_form()
	return render_template('login.html', title='Login', form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
	form = Registration_form()
	if form.validate_on_submit():
		flash("Your account has been registered. You can now login!","success")
		return redirect(url_for("login"))
	return render_template('signup.html', title='Signup', form = form)


if __name__ == '__main__':
	app.run(debug=True)