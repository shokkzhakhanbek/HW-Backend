from flask import Flask, redirect
from models import db
from books.routes import books_bp

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(books_bp)


@app.get("/")
def home():
    return redirect("/books/")


if __name__ == "__main__":
    app.run(debug=True)