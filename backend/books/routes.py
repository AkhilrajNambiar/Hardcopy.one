from flask import render_template, url_for, flash, redirect, request, Blueprint
from backend import db
from backend.books.forms import BookUploadForm, BookRequestForm
from backend.models import Book, Cart, PendingRequests, StarValues
from flask_login import current_user, login_required
from sqlalchemy import and_
from backend.users.utils import save_picture_without_compression
from backend.books.utils import book_search
import requests
from bs4 import BeautifulSoup

books = Blueprint('books', __name__)


@books.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = BookUploadForm()
    if form.validate_on_submit():
        pending = PendingRequests.query.all()
        pending_books = []
        for book in pending:
            pending_books.append(book.book_name)
        if form.book_name.data in pending_books:
            uploaded_book = PendingRequests.query.filter_by(book_name=form.book_name.data)
            db.session.delete(uploaded_book[0])
            db.session.commit()
        book = Book(book_name=form.book_name.data, author_name=form.author_name.data, genre=form.genre.data,
                    sub_genre=form.sub_genre.data, book_front=save_picture_without_compression(form.book_front.data),
                    book_back=save_picture_without_compression(form.book_back.data),
                    book_top=save_picture_without_compression(form.book_top.data),
                    book_bottom=save_picture_without_compression(form.book_bottom.data),
                    book_right=save_picture_without_compression(form.book_right.data),
                    book_left=save_picture_without_compression(form.book_left.data), provided_by=current_user)
        db.session.add(book)
        db.session.commit()
        stars = StarValues(book_id=book.id, donor_id=current_user.id)
        db.session.add(stars)
        db.session.commit()
        flash("Book has been successfully uploaded. Thank you for your contribution!", "success")
        return redirect(url_for('main.home'))
    return render_template('upload.html', title="Upload Books here", form=form)


stars = {}

@books.route('/book_page/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book_page(book_id):
    book = Book.query.get_or_404(book_id)
    starring = StarValues.query.filter_by(book_id=book.id).first()
    other_books_by_author = Book.query.filter_by(author_name=book.author_name)
    in_the_cart = False

    if current_user.is_authenticated:
        hai_ya_nahi = Cart.query.filter(and_(Cart.user_id == current_user.id, Cart.book_id == book_id))
        if hai_ya_nahi.count() == 1:
            in_the_cart = True

    ratings = StarValues.query.all()
    raters_list = []
    for i in ratings:
        raters_list.append(i.rater_id)

    if request.method == 'POST':
        if starring.donor_id != current_user.id and current_user.id not in raters_list:
            starring.rater_id = current_user.id
            if 'rating_content' in request.form:
                content = int(request.form['rating_content'])
                if content:
                    if content == 5:
                        starring.five_star_content += 1
                    elif content == 4:
                        starring.four_star_content += 1
                    elif content == 3:
                        starring.three_star_content += 1
                    elif content == 2:
                        starring.two_star_content += 1                    
                    elif content == 1:
                        starring.one_star_content += 1
                    # global votes_for_content, total_content_rating
                    book.votes_for_content += 1
                    book.total_content_rating += content
                    book.content_rating = float('{0:.1f}'.format(book.total_content_rating/book.votes_for_content))
                    db.session.commit()
                # book.content_rating = 0
                # db.session.commit()
            if 'rating_condition' in request.form:
                condition = int(request.form['rating_condition'])
                if condition:
                    # global votes_for_condition, total_condition_rating
                    if condition == 5:
                        starring.five_star_condition += 1
                    elif condition == 4:
                        starring.four_star_condition += 1
                    elif condition == 3:
                        starring.three_star_condition += 1
                    elif condition == 2:
                        starring.two_star_condition += 1                    
                    elif condition == 1:
                        starring.one_star_condition += 1
                    book.votes_for_condition += 1
                    book.total_condition_rating += condition
                    book.condition_rating = float('{0:.1f}'.format(book.total_condition_rating/book.votes_for_condition))
                    db.session.commit()
        elif starring.donor_id == current_user.id:
            flash('You cannot rate the book you donated!','warning')                    
            return redirect(url_for('books.book_page', book_id=book.id))

        elif current_user.id in raters_list:
            flash('You have already voted for this book! Please choose another one','warning')
            return redirect(url_for('books.book_page', book_id=book.id))
            # book.condition_rating = 0
            # db.session.commit()
    return render_template('book_page.html', title=book.book_name, book=book,
                           other_books_by_author=other_books_by_author, in_the_cart=in_the_cart, five_star_content=starring.five_star_content, four_star_content=starring.four_star_content, three_star_content=starring.three_star_content, two_star_content=starring.two_star_content, one_star_content=starring.one_star_content, five_star_condition=starring.five_star_condition, four_star_condition=starring.four_star_condition, three_star_condition=starring.three_star_condition, two_star_condition=starring.two_star_condition, one_star_condition=starring.one_star_condition, votes_for_condition=book.votes_for_condition, votes_for_content=book.votes_for_content)


@books.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('searchbar')
    matched_books = book_search(query)
    return render_template('search_results.html', title=f'Search result for {query}', matched_books=matched_books,
                           query=query)


@books.route('/fiction', methods=['GET', 'POST'])
def fiction():
    books = Book.query.all()
    return render_template('fiction.html', title='Fiction', books=books)


@books.route('/non_fiction', methods=['GET', 'POST'])
def non_fiction():
    books = Book.query.all()
    return render_template('non-fiction.html', title='Non-fiction', books=books)


@books.route('/biography', methods=['GET', 'POST'])
def biography():
    books = Book.query.all()
    return render_template('biography.html', title='Biography', books=books)


@books.route('/comics', methods=['GET', 'POST'])
def comics():
    books = Book.query.all()
    return render_template('comics.html', title='Comics', books=books)


@books.route('/romance', methods=['GET', 'POST'])
def romance():
    books = Book.query.all()
    return render_template('romance.html', title='Romance', books=books)


@books.route('/personality', methods=['GET', 'POST'])
def personality():
    books = Book.query.all()
    return render_template('personality.html', title='Self-Help', books=books)


@books.route('/request_book', methods=['GET', 'POST'])
@login_required
def request_book():
    form = BookRequestForm()
    if form.validate_on_submit():
        books = Book.query.all()
        book_names = []
        # global pending_requests
        for book in books:
            book_names.append(book.book_name)
        if form.book_name.data not in book_names:
            pending_requests = PendingRequests(book_name=form.book_name.data, author_name=form.author_name.data,
                                               user_id=current_user.id)
            db.session.add(pending_requests)
            db.session.commit()
            flash('Request successfully posted!', 'success')
            return redirect(url_for('books.request_book'))
        else:
            flash('The book already exists in our website. Please check!', 'danger')
    return render_template('request.html', title='Community', form=form, pending_requests=PendingRequests.query.all())
