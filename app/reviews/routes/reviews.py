# from flask import request, redirect, url_for, flash
# from flask_login import login_required, current_user
# from app.models import db, Book, Review, ReviewLike

# # Show book with reviews
# @books_bp.route("/books/<int:book_id>")
# def book_detail(book_id):
#     book = Book.query.get_or_404(book_id)
#     # Only show reviews where rating > 5
#     reviews = Review.query.filter(Review.book_id == book_id, Review.rating > 5).all()
#     return render_template("books/book_detail.html", book=book, reviews=reviews)

# # Add a review
# @books_bp.route("/books/<int:book_id>/add_review", methods=["POST"])
# @login_required
# def add_review(book_id):
#     rating = int(request.form.get("rating"))
#     text = request.form.get("text")

#     if rating < 1 or rating > 10:
#         flash("Rating must be between 1 and 10", "danger")
#         return redirect(url_for("books.book_detail", book_id=book_id))

#     review = Review(
#         rating=rating,
#         text=text,
#         user_id=current_user.id,
#         book_id=book_id,
#     )
#     db.session.add(review)
#     db.session.commit()
#     flash("Review added successfully!", "success")
#     return redirect(url_for("books.book_detail", book_id=book_id))

# # Like / dislike review
# @books_bp.route("/reviews/<int:review_id>/like/<string:action>", methods=["POST"])
# @login_required
# def like_review(review_id, action):
#     review = Review.query.get_or_404(review_id)
#     existing_like = ReviewLike.query.filter_by(user_id=current_user.id, review_id=review_id).first()

#     if existing_like:
#         # Update if action changes
#         existing_like.is_like = (action == "like")
#     else:
#         new_like = ReviewLike(
#             is_like=(action == "like"),
#             user_id=current_user.id,
#             review_id=review_id
#         )
#         db.session.add(new_like)

#     db.session.commit()
#     return redirect(url_for("books.book_detail", book_id=review.book_id))
