"""
BookService - Business logic layer for Book entity.
Controllers MUST NOT call DAO directly; they call BookService,
and BookService calls BookRepository.
"""

from dao.book_repository import BookRepository
from dao.author_repository import AuthorRepository
from models.book import Book


class BookService:
    """Service class encapsulating business logic for Book CRUD operations."""

    def __init__(self):
        self.book_repo = BookRepository()
        self.author_repo = AuthorRepository()

    def get_all_books(self):
        """Get all books with partial author info for the list view."""
        return self.book_repo.get_all()

    def get_book_by_id(self, book_id: int):
        """
        Get a book by ID with full author details attached.
        Returns the Book object with its Author relationship populated.
        """
        book = self.book_repo.get_by_id(book_id)
        if book is None:
            return None
        # Attach the full Author object for the detail view
        book.author = self.author_repo.get_by_id(book.author_id)
        return book

    def create_book(self, title: str, published_year: int, author_id: int):
        """
        Create a new book record.
        Validates input and delegates to the repository.
        """
        if not title or not title.strip():
            raise ValueError("Назва книги не може бути порожньою")
        if published_year is None:
            raise ValueError("Рік публікації є обов'язковим")

        book = Book(
            title=title.strip(),
            published_year=published_year,
            author_id=author_id
        )
        new_id = self.book_repo.create(book)
        book.id = new_id
        return book

    def update_book(self, book_id: int, title: str, published_year: int, author_id: int):
        """
        Update an existing book record.
        Validates input and delegates to the repository.
        """
        if not title or not title.strip():
            raise ValueError("Назва книги не може бути порожньою")
        if published_year is None:
            raise ValueError("Рік публікації є обов'язковим")

        book = Book(
            id=book_id,
            title=title.strip(),
            published_year=published_year,
            author_id=author_id
        )
        return self.book_repo.update(book)

    def delete_book(self, book_id: int):
        """Delete a book record by ID."""
        return self.book_repo.delete(book_id)
