from flask import Blueprint, render_template, request, redirect, url_for

from services.book_service import BookService
from services.author_service import AuthorService

book_bp = Blueprint("books", __name__)

book_service = BookService()
author_service = AuthorService()


@book_bp.route("/")
def index():
    return redirect(url_for("books.book_list"))


@book_bp.route("/books")
def book_list():
    try:
        books = book_service.get_all_books()
        return render_template("book_list.html", books=books)
    except Exception:
        return render_template("error.html"), 500


@book_bp.route("/books/new", methods=["GET", "POST"])
def book_create():
    try:
        if request.method == "POST":
            title = request.form.get("title", "")
            published_year = int(request.form.get("published_year", 0))
            author_id = int(request.form.get("author_id", 0))

            book_service.create_book(title, published_year, author_id)
            return redirect(url_for("books.book_list"))

        authors = author_service.get_all_authors()
        return render_template("book_form.html", book=None, authors=authors)
    except Exception:
        return render_template("error.html"), 500


@book_bp.route("/books/<int:book_id>")
def book_detail(book_id):
    try:
        book = book_service.get_book_by_id(book_id)
        if book is None:
            return render_template("error.html", message="Книгу не знайдено"), 404
        return render_template("book_detail.html", book=book)
    except Exception:
        return render_template("error.html"), 500


@book_bp.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def book_edit(book_id):
    try:
        if request.method == "POST":
            title = request.form.get("title", "")
            published_year = int(request.form.get("published_year", 0))
            author_id = int(request.form.get("author_id", 0))

            book_service.update_book(book_id, title, published_year, author_id)
            return redirect(url_for("books.book_detail", book_id=book_id))

        book = book_service.get_book_by_id(book_id)
        if book is None:
            return render_template("error.html", message="Книгу не знайдено"), 404
        authors = author_service.get_all_authors()
        return render_template("book_form.html", book=book, authors=authors)
    except Exception:
        return render_template("error.html"), 500


@book_bp.route("/books/<int:book_id>/delete", methods=["POST"])
def book_delete(book_id):
    try:
        book_service.delete_book(book_id)
        return redirect(url_for("books.book_list"))
    except Exception:
        return render_template("error.html"), 500
