from backend.models import Book

def book_search(query):
    matched_books = []
    # query = query.capitalize()
    book_list = Book.query.all()
    for i in book_list:
        if query in i.book_name or query in i.genre or query in i.author_name or query in i.sub_genre:
            matched_books.append(i)
    return matched_books