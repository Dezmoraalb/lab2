from dao.book_repository import BookRepository
from dao.author_repository import AuthorRepository
from models.book import Book


class BookService:

    def __init__(self):
        self.book_repo = BookRepository()
        self.author_repo = AuthorRepository()

    def get_all_books(self):
        return self.book_repo.get_all()

    def get_book_by_id(self, book_id: int):
        book = self.book_repo.get_by_id(book_id)
        if book is None:
            return None
        book.author = self.author_repo.get_by_id(book.author_id)
        return book

    def create_book(self, title: str, published_year: int, author_id: int):
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
        return self.book_repo.delete(book_id)
