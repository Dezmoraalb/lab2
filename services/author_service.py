"""
AuthorService - Business logic layer for Author entity.
Acts as an intermediary between Controllers and AuthorRepository.
"""

from dao.author_repository import AuthorRepository


class AuthorService:
    """Service class encapsulating business logic for Author operations."""

    def __init__(self):
        self.repository = AuthorRepository()

    def get_all_authors(self):
        """Retrieve all authors. Used to populate dropdowns in forms."""
        return self.repository.get_all()

    def get_author_by_id(self, author_id: int):
        """Retrieve a single author by ID. Used when displaying book details."""
        return self.repository.get_by_id(author_id)
