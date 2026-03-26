from database.db import get_connection
from models.author import Author


class AuthorRepository:

    def get_all(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, full_name, bio FROM authors ORDER BY full_name")
            rows = cursor.fetchall()
            return [Author.from_row(row) for row in rows]
        finally:
            conn.close()

    def get_by_id(self, author_id: int):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, full_name, bio FROM authors WHERE id = ?", (author_id,))
            row = cursor.fetchone()
            return Author.from_row(row)
        finally:
            conn.close()
