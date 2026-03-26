"""
AuthorRepository - Data Access Object for the Author entity.
Contains raw SQL queries for reading author records from SQLite3.
Authors are pre-populated (seed data), so only read operations are needed.
"""

from database.db import get_connection
from models.author import Author


class AuthorRepository:
    """Repository class providing data access methods for Author entity."""

    def get_all(self):
        """Fetch all authors from the database, ordered by full name."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, full_name, bio FROM authors ORDER BY full_name")
            rows = cursor.fetchall()
            return [Author.from_row(row) for row in rows]
        finally:
            conn.close()

    def get_by_id(self, author_id: int):
        """Fetch a single author by ID. Returns None if not found."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, full_name, bio FROM authors WHERE id = ?", (author_id,))
            row = cursor.fetchone()
            return Author.from_row(row)
        finally:
            conn.close()
