import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "library.db")


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            bio TEXT NOT NULL DEFAULT ''
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            published_year INTEGER NOT NULL,
            author_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES authors(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM authors")
    count = cursor.fetchone()[0]

    if count == 0:
        seed_authors = [
            ("Тарас Шевченко", "Український поет, письменник, художник, громадський діяч. "
                               "Автор збірки «Кобзар» та багатьох інших творів."),
            ("Леся Українка", "Українська письменниця, поетеса, перекладачка, культурна діячка. "
                              "Авторка драматичних поем «Лісова пісня» та «Бояриня»."),
            ("Іван Франко", "Український письменник, поет, публіцист, перекладач, вчений. "
                            "Автор повісті «Захар Беркут» та поеми «Мойсей»."),
        ]
        cursor.executemany(
            "INSERT INTO authors (full_name, bio) VALUES (?, ?)",
            seed_authors
        )

    conn.commit()
    conn.close()
