"""
Book Controller - Flask Blueprint handling HTTP requests for Book CRUD.
All routes use try-except blocks to catch errors and render a user-friendly
error page instead of exposing internal server errors.
"""

from flask import Blueprint, render_template, request, redirect, url_for

from services.book_service import BookService
from services.author_service import AuthorService

# Create a Flask Blueprint for book-related routes
book_bp = Blueprint("books", __name__)

# Instantiate services (controllers call services, never DAO directly)
book_service = BookService()
author_service = AuthorService()


@book_bp.route("/")
def index():
    """Redirect root URL to the books list page."""
    return redirect(url_for("books.book_list"))


@book_bp.route("/books")
def book_list():
    """
    List Page — displays a table of all books.
    Shows partial author info (author name only).
    Contains buttons for Create, Edit, Delete.
    """
    try:
        books = book_service.get_all_books()
        return render_template("book_list.html", books=books)
    except Exception:
        return render_template("error.html"), 500


@book_bp.route("/books/new", methods=["GET", "POST"])
def book_create():
    """
    Create Page — form to add a new book.
    GET: display the form with author dropdown.
    POST: process the form and create the book.
    """
    try:
        if request.method == "POST":
            title = request.form.get("title", "")
            published_year = int(request.form.get("published_year", 0))
            author_id = int(request.form.get("author_id", 0))

            book_service.create_book(title, published_year, author_id)
            return redirect(url_for("books.book_list"))

        # GET: render the form
        authors = author_service.get_all_authors()
        return render_template("book_form.html", book=None, authors=authors)
    except Exception:
        return render_template("error.html"), 500


@book_bp.route("/books/<int:book_id>")
def book_detail(book_id):
    """
    Detail Page — displays full book info with full author details (name + bio).
    """
    try:
        book = book_service.get_book_by_id(book_id)
        if book is None:
            return render_template("error.html", message="Книгу не знайдено"), 404
        return render_template("book_detail.html", book=book)
    except Exception:
        return render_template("error.html"), 500


@book_bp.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def book_edit(book_id):
    """
    Edit Page — form to update an existing book.
    GET: display the form pre-filled with current data.
    POST: process the form and update the book.
    """
    try:
        if request.method == "POST":
            title = request.form.get("title", "")
            published_year = int(request.form.get("published_year", 0))
            author_id = int(request.form.get("author_id", 0))

            book_service.update_book(book_id, title, published_year, author_id)
            return redirect(url_for("books.book_detail", book_id=book_id))

        # GET: load current book data and authors for the form
        book = book_service.get_book_by_id(book_id)
        if book is None:
            return render_template("error.html", message="Книгу не знайдено"), 404
        authors = author_service.get_all_authors()
        return render_template("book_form.html", book=book, authors=authors)
    except Exception:
        return render_template("error.html"), 500


@book_bp.route("/books/<int:book_id>/delete", methods=["POST"])
def book_delete(book_id):
    """
    Delete action — removes a book and redirects to the list.
    Only accepts POST requests to prevent accidental deletion via GET.
    """
    try:
        book_service.delete_book(book_id)
        return redirect(url_for("books.book_list"))
    except Exception:
        return render_template("error.html"), 500
