from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from backend.models import User
from flask_login import current_user

country_list = ["Please Select...","AF|Afghanistan","AL|Albania","DZ|Algeria","AS|American Samoa","AD|Andorra","AO|Angola","AI|Anguilla","AQ|Antarctica","AG|Antigua And Barbuda","AR|Argentina","AM|Armenia","AW|Aruba","AU|Australia","AT|Austria","AZ|Azerbaijan","BS|Bahamas","BH|Bahrain","BD|Bangladesh","BB|Barbados","BY|Belarus","BE|Belgium","BZ|Belize","BJ|Benin","BM|Bermuda","BT|Bhutan","BO|Bolivia","BA|Bosnia And Herzegovina","BW|Botswana","BV|Bouvet Island","BR|Brazil","IO|British Indian Ocean Territory","BN|Brunei Darussalam","BG|Bulgaria","BF|Burkina Faso","BI|Burundi","KH|Cambodia","CM|Cameroon","CA|Canada","CV|Cape Verde","KY|Cayman Islands","CF|Central African Republic","TD|Chad","CL|Chile","CN|China","CX|Christmas Island","CC|Cocos (keeling) Islands","CO|Colombia","KM|Comoros","CG|Congo","CD|Congo, The Democratic Republic Of The","CK|Cook Islands","CR|Costa Rica","CI|Cote D'ivoire","HR|Croatia","CU|Cuba","CY|Cyprus","CZ|Czech Republic","DK|Denmark","DJ|Djibouti","DM|Dominica","DO|Dominican Republic","TP|East Timor","EC|Ecuador","EG|Egypt","SV|El Salvador","GQ|Equatorial Guinea","ER|Eritrea","EE|Estonia","ET|Ethiopia","FK|Falkland Islands (malvinas)","FO|Faroe Islands","FJ|Fiji","FI|Finland","FR|France","GF|French Guiana","PF|French Polynesia","TF|French Southern Territories","GA|Gabon","GM|Gambia","GE|Georgia","DE|Germany","GH|Ghana","GI|Gibraltar","GR|Greece","GL|Greenland","GD|Grenada","GP|Guadeloupe","GU|Guam","GT|Guatemala","GN|Guinea","GW|Guinea-bissau","GY|Guyana","HT|Haiti","HM|Heard Island And Mcdonald Islands","VA|Holy See (vatican City State)","HN|Honduras","HK|Hong Kong","HU|Hungary","IS|Iceland","IN|India","ID|Indonesia","IR|Iran","IQ|Iraq","IE|Ireland","IL|Israel","IT|Italy","JM|Jamaica","JP|Japan","JO|Jordan","KZ|Kazakstan","KE|Kenya","KI|Kiribati","KP|Korea, Democratic People's Republic Of","KR|Korea, Republic Of","KV|Kosovo","KW|Kuwait","KG|Kyrgyzstan","LA|Lao People's Democratic Republic","LV|Latvia","LB|Lebanon","LS|Lesotho","LR|Liberia","LY|Libyan Arab Jamahiriya","LI|Liechtenstein","LT|Lithuania","LU|Luxembourg","MO|Macau","MK|Macedonia, The Former Yugoslav Republic Of","MG|Madagascar","MW|Malawi","MY|Malaysia","MV|Maldives","ML|Mali","MT|Malta","MH|Marshall Islands","MQ|Martinique","MR|Mauritania","MU|Mauritius","YT|Mayotte","MX|Mexico","FM|Micronesia, Federated States Of","MD|Moldova, Republic Of","MC|Monaco","MN|Mongolia","MS|Montserrat","ME|Montenegro","MA|Morocco","MZ|Mozambique","MM|Myanmar","NA|Namibia","NR|Nauru","NP|Nepal","NL|Netherlands","AN|Netherlands Antilles","NC|New Caledonia","NZ|New Zealand","NI|Nicaragua","NE|Niger","NG|Nigeria","NU|Niue","NF|Norfolk Island","MP|Northern Mariana Islands","NO|Norway","OM|Oman","PK|Pakistan","PW|Palau","PS|Palestinian Territory, Occupied","PA|Panama","PG|Papua New Guinea","PY|Paraguay","PE|Peru","PH|Philippines","PN|Pitcairn","PL|Poland","PT|Portugal","PR|Puerto Rico","QA|Qatar","RE|Reunion","RO|Romania","RU|Russian Federation","RW|Rwanda","SH|Saint Helena","KN|Saint Kitts And Nevis","LC|Saint Lucia","PM|Saint Pierre And Miquelon","VC|Saint Vincent And The Grenadines","WS|Samoa","SM|San Marino","ST|Sao Tome And Principe","SA|Saudi Arabia","SN|Senegal","RS|Serbia","SC|Seychelles","SL|Sierra Leone","SG|Singapore","SK|Slovakia","SI|Slovenia","SB|Solomon Islands","SO|Somalia","ZA|South Africa","GS|South Georgia And The South Sandwich Islands","ES|Spain","LK|Sri Lanka","SD|Sudan","SR|Suriname","SJ|Svalbard And Jan Mayen","SZ|Swaziland","SE|Sweden","CH|Switzerland","SY|Syrian Arab Republic","TW|Taiwan, Province Of China","TJ|Tajikistan","TZ|Tanzania, United Republic Of","TH|Thailand","TG|Togo","TK|Tokelau","TO|Tonga","TT|Trinidad And Tobago","TN|Tunisia","TR|Turkey","TM|Turkmenistan","TC|Turks And Caicos Islands","TV|Tuvalu","UG|Uganda","UA|Ukraine","AE|United Arab Emirates","GB|United Kingdom","US|United States","UM|United States Minor Outlying Islands","UY|Uruguay","UZ|Uzbekistan","VU|Vanuatu","VE|Venezuela","VN|Viet Nam","VG|Virgin Islands, British","VI|Virgin Islands, U.s.","WF|Wallis And Futuna","EH|Western Sahara","YE|Yemen","ZM|Zambia","ZW|Zimbabwe"]

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