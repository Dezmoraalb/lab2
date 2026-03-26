"""
BookRepository - Data Access Object for the Book entity.
Contains raw SQL queries for full CRUD operations on SQLite3.
"""

from database.db import get_connection
from models.book import Book


class BookRepository:
    """Repository class providing CRUD data access methods for Book entity."""

    def get_all(self):
        """
        Fetch all books with their author's full name.
        Uses JOIN to include partial author info for the list view.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.id, b.title, b.published_year, b.author_id, a.full_name AS author_name
                FROM books b
                JOIN authors a ON b.author_id = a.id
                ORDER BY b.title
            """)
            rows = cursor.fetchall()
            books = []
            for row in rows:
                book = Book.from_row(row)
                # Attach author name as an extra attribute for display
                book.author_name = row["author_name"]
                books.append(book)
            return books
        finally:
            conn.close()

    def get_by_id(self, book_id: int):
        """Fetch a single book by ID. Returns None if not found."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, published_year, author_id
                FROM books
                WHERE id = ?
            """, (book_id,))
            row = cursor.fetchone()
            return Book.from_row(row)
        finally:
            conn.close()

    def create(self, book: Book):
        """Insert a new book record into the database. Returns the new book's ID."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO books (title, published_year, author_id)
                VALUES (?, ?, ?)
            """, (book.title, book.published_year, book.author_id))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def update(self, book: Book):
        """Update an existing book record by ID."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE books
                SET title = ?, published_year = ?, author_id = ?
                WHERE id = ?
            """, (book.title, book.published_year, book.author_id, book.id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def delete(self, book_id: int):
        """Delete a book record by ID."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
