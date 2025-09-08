from flask import Blueprint, render_template
from app.models import Book, BuyRequest

# Define blueprint
main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    listings = Book.query.order_by(Book.created_at.desc()).limit(12).all()
    buy_requests = BuyRequest.query.order_by(BuyRequest.created_at.desc()).limit(10).all()
    return render_template("main/index.html", listings=listings, buy_requests=buy_requests)

@main_bp.route("/privacy")
def privacy():
    return render_template("main/privacy_policy.html")

@main_bp.route("/terms")
def terms():
    return render_template("main/terms.html")

@main_bp.route("/about")
def about():
    return render_template("main/about.html")
