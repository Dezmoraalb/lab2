class Author:
    def __init__(self, id: int = None, full_name: str = "", bio: str = ""):
        self.id = id
        self.full_name = full_name
        self.bio = bio

    def __repr__(self):
        return f"Author(id={self.id}, full_name='{self.full_name}')"

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return Author(
            id=row["id"],
            full_name=row["full_name"],
            bio=row["bio"]
        )
