from backend.models import Book

def book_search(query):
    matched_books = []
    query = query.lower()
    book_list = Book.query.all()
    for i in book_list:
        if query in i.book_name.lower() or query in i.genre.lower() or query in i.author_name.lower() or query in i.sub_genre.lower():
            if query == 'fiction' and i.genre.lower() == 'non-fiction':
                continue
            matched_books.append(i)
    return matched_books

