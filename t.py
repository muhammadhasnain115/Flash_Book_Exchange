from app import create_app, db
from app.models import User, Book, Review, Wishlist, BuyRequest, Donation

app = create_app()
with app.app_context():
    db.create_all()
