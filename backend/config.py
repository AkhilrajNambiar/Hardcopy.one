import os
import json

with open('/etc/config.json') as config_file:
	config = json.load(config_file)


class Config:
	SECRET_KEY = config.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = config.get('EMAIL_USER')
	MAIL_PASSWORD = config.get('EMAIL_PASS')
	STRIPE_PUBLIC_KEY = config.get('STRIPE_PUBLIC_KEY')
	STRIPE_SECRET_KEY = config.get('STRIPE_SECRET_KEY')
	SHIPROCKET_TOKEN = config.get('SHIPROCKET_TOKEN')
