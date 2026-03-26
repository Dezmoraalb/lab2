"""
app.py - Application entry point.
Initializes the Flask app, registers blueprints, and starts the server.
The database is initialized on first run (tables + seed data).
"""

from flask import Flask
from database.db import init_db
from controllers.book_controller import book_bp


def create_app():
    """Application factory: creates and configures the Flask app."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "library-secret-key-2064"

    # Register the book controller blueprint
    app.register_blueprint(book_bp)

    # Initialize the database (create tables & seed data if needed)
    with app.app_context():
        init_db()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
