from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Book

books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.get("/")
def books_list():
    books = Book.query.order_by(Book.id.desc()).all()
    return render_template("books/index.html", books=books)


@books_bp.get("/<int:book_id>")
def books_show(book_id: int):
    book = Book.query.get(book_id)
    if not book:
        return "Not Found", 404
    return render_template("books/show.html", book=book)


@books_bp.get("/<int:book_id>/edit")
def books_edit_form(book_id: int):
    book = Book.query.get(book_id)
    if not book:
        return "Not Found", 404
    return render_template("books/edit.html", book=book)


@books_bp.post("/<int:book_id>/edit")
def books_edit_submit(book_id: int):
    book = Book.query.get(book_id)
    if not book:
        return "Not Found", 404

    book.title = request.form.get("title", "").strip()
    book.author = request.form.get("author", "").strip()
    book.year = int(request.form.get("year", 0))
    book.total_pages = int(request.form.get("total_pages", 0))
    book.genre = request.form.get("genre", "").strip()

    db.session.commit()
    return redirect(url_for("books.books_show", book_id=book.id))


@books_bp.post("/<int:book_id>/delete")
def books_delete(book_id: int):
    book = Book.query.get(book_id)
    if not book:
        return "Not Found", 404

    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("books.books_list"))