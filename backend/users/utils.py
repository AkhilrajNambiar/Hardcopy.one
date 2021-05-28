import secrets
import os
from PIL import Image
from flask import url_for
from backend import app, mail
from flask_mail import Message
from backend.models import Book


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


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f"""To reset the password go to following link:
{url_for('users.reset_password', token=token, _external=True)}
If you did not make this request, please ignore this message and there won't be any changes made!
"""
    mail.send(msg)

