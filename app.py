from flask import Flask
from database.db import init_db
from controllers.book_controller import book_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "library-secret-key-2026"

    app.register_blueprint(book_bp)

    with app.app_context():
        init_db()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
