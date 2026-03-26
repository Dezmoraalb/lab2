"""
Database connection management module.
Provides functions to get a database connection and initialize the schema.
Uses sqlite3 with Row factory for convenient dict-like access to rows.
"""

import sqlite3
import os

# Path to the SQLite database file (stored at the project root)
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "library.db")


def get_connection():
    """
    Create and return a new SQLite3 database connection.
    Enables foreign key support and uses Row factory for named column access.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """
    Initialize the database schema and seed data.
    Creates tables if they don't exist and inserts sample author records.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Create the 'authors' table (auxiliary entity)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            bio TEXT NOT NULL DEFAULT ''
        )
    """)

    # Create the 'books' table (main entity) with FK to authors
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

    # Seed authors only if the table is empty (first run)
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
