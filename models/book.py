class Book:
    def __init__(self, id: int = None, title: str = "", published_year: int = None,
                 author_id: int = None, author=None):
        self.id = id
        self.title = title
        self.published_year = published_year
        self.author_id = author_id
        self.author = author

    def __repr__(self):
        return f"Book(id={self.id}, title='{self.title}', year={self.published_year})"

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return Book(
            id=row["id"],
            title=row["title"],
            published_year=row["published_year"],
            author_id=row["author_id"]
        )
