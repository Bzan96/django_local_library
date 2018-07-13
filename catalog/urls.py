from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # To reach this link the URL will already have gone through the other url.py, where
    # it gets linked to /catalog. So this is really /catalog/books!
    path("books/", views.BookListView.as_view(), name="books"),
    path("book/<int:pk>", views.BookDetailView.as_view(), name="book-detail"),
    path("authors/", views.AuthorListView.as_view(), name="authors"),
    path("author/<int:pk>", views.AuthorDetailView.as_view(), name="author-detail"),
]

# Shows a user specific list of loaned books
urlpatterns += [
    path("mybooks/", views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),
]

# Shows a list of all loaned books, available for view only by staff. Also allows staff to renew loans.
urlpatterns += [    
    path("loanedbooks/", views.LoanedBooksListView.as_view(), name="all-borrowed"),
    path("book/<uuid:pk>/renew/", views.renew_book_librarian, name="renew-book-librarian"),
]

# Allows staff to create, update or delete an author.
# We're using <int:pk> on the two latter because by then we're referencing a specific author: primary key
urlpatterns += [
    path("author/create/", views.AuthorCreate.as_view(), name="author_create"),
    path("author/<int:pk>/update/", views.AuthorUpdate.as_view(), name="author_update"),
    path("author/<int:pk>/delete/", views.AuthorDelete.as_view(), name="author_delete"),
]

# Allows staff to create, update or delete a book.
# We're using <int:pk> on the two latter because by then we're referencing a specific book: primary key
urlpatterns += [
    path("book/create/", views.BookCreate.as_view(), name="book_create"),
    path("book/<int:pk>/update/", views.BookUpdate.as_view(), name="book_update"),
    path("book/<int:pk>/delete/", views.BookDelete.as_view(), name="book_delete"),
]