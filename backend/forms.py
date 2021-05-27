from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from backend.models import User
from flask_login import current_user

country_list = ['Please select...','Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antigua And Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia And Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo-The Democratic Republic Of The', 'Cook Islands', 'Costa Rica', "Cote D'ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guinea-bissau', 'Guyana', 'Haiti', 'Heard Island And Mcdonald Islands', 'Holy See (vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakstan', 'Kenya', 'Kiribati', "Korea-Democratic People's Republic Of", 'Korea-Republic Of', 'Kosovo', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libyan Arab Jamahiriya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Macedonia-The Former Yugoslav Republic Of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia-Federated States Of', 'Moldova-Republic Of', 'Monaco', 'Mongolia', 'Montserrat', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'Netherlands Antilles', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory-Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Helena', 'Saint Kitts And Nevis', 'Saint Lucia', 'Saint Pierre And Miquelon', 'Saint Vincent And The Grenadines', 'Samoa', 'San Marino', 'Sao Tome And Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia And The South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Svalbard And Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan-Republic Of China', 'Tajikistan', 'Tanzania-United Republic Of', 'Thailand', 'Togo', 'Tokelau', 'Tonga', 'Trinidad And Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks And Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Virgin Islands-British', 'Virgin Islands-U.S.', 'Wallis And Futuna', 'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe']

class Registration_form(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email ID',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    street = StringField('Room No. and Street',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired()])
    state = StringField('State',validators=[DataRequired()])
    countries = SelectField('Country', choices=country_list, validators=[DataRequired()])
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email already exists. Please choose another one.')
class Login_form(FlaskForm):
    email = StringField('Email ID',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login!')

class Feedback_form(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email ID',validators=[DataRequired(), Email()])
    subject = StringField('Subject',validators=[DataRequired()])
    feedback = TextAreaField('Feedback/Criticism', validators=[DataRequired()])
    submit = SubmitField('Send Feedback')

class Update_form(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email ID',validators=[DataRequired(), Email()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another one.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose another one.')    

class BookUploadForm(FlaskForm):
    book_name = StringField('Book name', validators=[DataRequired()])
    author_name = StringField('Author/Publisher name', validators=[DataRequired()])
    genre = SelectField('Genre', validators=[DataRequired()], choices=['Please select...', 'Fiction', 'Non-fiction', 'Romance', 'Biography', 'Comics', 'Self-help'])
    sub_genre = SelectField('Sub-genre', validators=[DataRequired()], choices=['Please select...', 'Computers and Technology', 'Encyclopedias', 'History', 'Natural Sciences', 'Exam preparation', 'Commerce & Accounting', 'Religion & Spirituality'])
    book_front = FileField('Book Front', validators=[DataRequired(), FileAllowed(['jpg','png','jpeg'])])
    book_back = FileField('Book Back', validators=[DataRequired(), FileAllowed(['jpg','png','jpeg'])])    
    book_top = FileField('Book Top', validators=[DataRequired(), FileAllowed(['jpg','png','jpeg'])])
    book_bottom = FileField('Book Bottom', validators=[DataRequired(), FileAllowed(['jpg','png','jpeg'])])
    book_right = FileField('Book Right', validators=[DataRequired(), FileAllowed(['jpg','png','jpeg'])])
    book_left = FileField('Book Left', validators=[DataRequired(), FileAllowed(['jpg','png','jpeg'])])
    extras = TextAreaField('Anything else that the reader should know?', validators=[Length(max=300)])
    submit = SubmitField('Upload Book')

class BookRequestForm(FlaskForm):
    book_name = StringField('Book name', validators=[DataRequired()])
    author_name = StringField('Author/Publisher name', validators=[DataRequired()])
    submit = SubmitField('Request this Book')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class AddressUpdateForm(FlaskForm):
    street = StringField('Room No. and Street',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired()])
    state = StringField('State',validators=[DataRequired()])
    countries = SelectField('Country', choices=country_list, validators=[DataRequired()])
    submit = SubmitField('Update')


