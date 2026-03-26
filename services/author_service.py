from dao.author_repository import AuthorRepository


class AuthorService:

    def __init__(self):
        self.repository = AuthorRepository()

    def get_all_authors(self):
        return self.repository.get_all()

    def get_author_by_id(self, author_id: int):
        return self.repository.get_by_id(author_id)
