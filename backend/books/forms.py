from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

class BookUploadForm(FlaskForm):
    book_name = StringField('Book name', validators=[DataRequired()])
    author_name = StringField('Author/Publisher name', validators=[DataRequired()])
    genre = SelectField('Genre', validators=[DataRequired()], choices=['Please select...','Fiction', 'Non-fiction', 'Romance', 'Biography', 'Comics', 'Self-help'])
    sub_genre = SelectField('Sub-genre', validators=[DataRequired()], choices=['Please select...','Computers and Technology', 'Encyclopedias', 'History', 'Natural Sciences', 'Exam preparation', 'Commerce & Accounting', 'Religion & Spirituality'])
    book_front = FileField('Book Front', validators=[DataRequired(), FileAllowed(['jpg','png','jpeg'])])
    book_back = FileField('Book Back', validators=[DataRequired(), FileAllowed(['jpg','png','jpeg'])])    
    book_top = FileField('Book Top', validators=[DataRequired(), FileAllowed(['jpg','png','jpeg'])])
    book_bottom = FileField('Book Bottom', validators=[DataRequired(), FileAllowed(['jpg','png','jpeg'])])
    book_right = FileField('Book Right', validators=[DataRequired(), FileAllowed(['jpg','png','jpeg'])])
    book_left = FileField('Book Left', validators=[DataRequired(), FileAllowed(['jpg','png','jpeg'])])
    length = StringField('Length(in cm)', validators=[DataRequired()])
    breadth= StringField('Breadth(in cm)', validators=[DataRequired()])
    height = StringField('Height(in cm)', validators=[DataRequired()])
    weight = StringField('Weight(in grms)', validators=[DataRequired()])    
    extras = TextAreaField('Anything else that the reader should know?', validators=[Length(max=300)])
    submit = SubmitField('Upload Book')
            

class BookRequestForm(FlaskForm):
    book_name = StringField('Book name', validators=[DataRequired()])
    author_name = StringField('Author/Publisher name', validators=[DataRequired()])
    submit = SubmitField('Request this Book')    