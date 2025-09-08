import os, uuid, secrets
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from app import db
from app.models import Book, Review, Wishlist, BuyRequest
from app.forms import BookForm, ReviewForm, BuyRequestForm
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime, date
from sqlalchemy.orm import joinedload

# ✅ Define Blueprint here
# app/books/routes.py
books_bp = Blueprint("books", __name__)


UPLOAD_FOLDER = os.path.join("app", "static", "uploads")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS




@books_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_book():
    # Count how many books this user has posted today
    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = datetime.combine(date.today(), datetime.max.time())
    user_books_today = Book.query.filter(
        Book.owner_id == current_user.id,
        Book.created_at >= today_start,
        Book.created_at <= today_end
    ).count()

    if user_books_today >= 10:
        flash("You can only post 10 books per day.", "warning")
        return redirect(url_for("books.browse"))

    form = BookForm()
    if form.validate_on_submit():
        filename = None

        if form.image.data and allowed_file(form.image.data.filename):
            ext = form.image.data.filename.rsplit(".", 1)[1].lower()
            filename = f"{current_user.id}_{uuid.uuid4().hex}.{ext}"
            save_path = os.path.join(current_app.root_path, "static/uploads", filename)
            form.image.data.save(save_path)

        price = None if form.is_free.data else form.price.data

        b = Book(
            title=form.title.data.strip(),
            author=form.author.data.strip() if form.author.data else None,
            condition=form.condition.data,
            is_free=form.is_free.data,
            price=price,
            category=form.category.data.strip() if form.category.data else None,
            location=form.location.data.strip() if form.location.data else None,
            image_file=filename,
            description=form.description.data.strip() if form.description.data else None,
            owner_id=current_user.id,
        )

        db.session.add(b)
        db.session.commit()
        flash("Listing published.", "success")
        return redirect(url_for("books.book_detail", book_id=b.id))

    return render_template("books/add_book.html", form=form)



@books_bp.route("/<int:book_id>", methods=["GET", "POST"])
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    form = ReviewForm()

    # Handle review submission
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Please login to leave a review.", "warning")
            return redirect(url_for("auth.login"))

        r = Review(
            rating=int(form.rating.data),
            comment=form.comment.data.strip() if form.comment.data else None,
            user_id=current_user.id,
            book_id=book.id,
        )
        db.session.add(r)
        db.session.commit()
        flash("Thanks for the review.", "success")
        return redirect(url_for("books.book_detail", book_id=book.id))

    # Check if the current user has wishlisted this book
    wished = False
    if current_user.is_authenticated:
        wished = Wishlist.query.filter_by(user_id=current_user.id, book_id=book.id).first() is not None

    # Calculate average rating and reviews
    avg = book.avg_rating()
    reviews = book.reviews.order_by(Review.created_at.desc()).all()

    return render_template("books/book_detail.html", book=book, form=form, wished=wished, avg=avg, reviews=reviews)

@books_bp.route("/toggle-wishlist/<int:book_id>", methods=["POST"])
@login_required
def toggle_wishlist(book_id):
    book = Book.query.get_or_404(book_id)
    item = Wishlist.query.filter_by(user_id=current_user.id, book_id=book.id).first()

    if item:
        # Remove from wishlist
        db.session.delete(item)
        db.session.commit()
        return jsonify({"status": "removed"})
    else:
        # Add to wishlist
        w = Wishlist(user_id=current_user.id, book_id=book.id)
        db.session.add(w)
        db.session.commit()
        return jsonify({"status": "added"})


@books_bp.route("/browse")
def browse():
    q = request.args.get("q", "")
    condition = request.args.get("condition", "")
    free = request.args.get("free") == "1"
    category = request.args.get("category", "")

    books = Book.query
    if q:
        like = f"%{q}%"
        books = books.filter(Book.title.ilike(like) | Book.author.ilike(like) | Book.description.ilike(like))
    if condition in ("new", "used"):
        books = books.filter_by(condition=condition)
    if free:
        books = books.filter_by(is_free=True)
    if category:
        books = books.filter(Book.category.ilike(f"%{category}%"))

    books = books.order_by(Book.created_at.desc()).limit(100).all()
    return render_template("books/list_books.html", books=books)


@books_bp.route("/buyrequest/new", methods=["GET", "POST"])
@login_required
def create_buyrequest():
    # Count how many buy requests this user has posted today
    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = datetime.combine(date.today(), datetime.max.time())
    user_requests_today = BuyRequest.query.filter(
        BuyRequest.user_id == current_user.id,
        BuyRequest.created_at >= today_start,
        BuyRequest.created_at <= today_end
    ).count()

    if user_requests_today >= 10:
        flash("You can only post 10 buy requests per day.", "warning")
        return redirect(url_for("books.buy_requests"))

    form = BuyRequestForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(secure_filename(form.image.data.filename))
            filename = random_hex + f_ext
            filepath = os.path.join(current_app.root_path, "static/uploads", filename)
            form.image.data.save(filepath)

        buy_request = BuyRequest(
            title=form.title.data,
            author=form.author.data,
            details=form.details.data,
            budget=None if form.is_free.data else form.budget.data,
            is_free=form.is_free.data,
            location=form.location.data,
            image_file=filename,
            user_id=current_user.id
        )

        db.session.add(buy_request)
        db.session.commit()
        flash("Your buy request has been posted!", "success")
        return redirect(url_for("books.buy_requests"))

    return render_template("books/create_buy_requests.html", form=form)



@books_bp.route("/buy-requests")
def buy_requests():
    requests = BuyRequest.query.order_by(BuyRequest.created_at.desc()).limit(50).all()
    return render_template("books/buy_requests.html", requests=requests)


@books_bp.route("/buyrequest/<int:request_id>")
def buy_request_detail(request_id):
    buy_request = BuyRequest.query.get_or_404(request_id)
    print("DEBUG:", buy_request.user)        # Should not be None
    if buy_request.user:
        print("DEBUG phone:", buy_request.user.phone)

    return render_template("books/buy_request_detail.html", buy_request=buy_request)
