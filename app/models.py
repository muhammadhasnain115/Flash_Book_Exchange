from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    email = db.Column(db.String(140), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Optional avatar
    avatar_file = db.Column(db.String(200), default=None)

    # Relationships
    listings = db.relationship("Book", backref="owner", lazy="dynamic", cascade="all,delete")
    reviews = db.relationship("Review", backref="author", lazy="dynamic", cascade="all,delete")
    wishlist = db.relationship("Wishlist", backref="user", lazy="dynamic", cascade="all,delete")
    donations = db.relationship("Donation", backref="donor", lazy="dynamic", cascade="all,delete")
    # buy_requests backref will be defined in BuyRequest

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100))
    price = db.Column(db.Float)
    is_free = db.Column(db.Boolean, default=False)
    condition = db.Column(db.String(20))
    category = db.Column(db.String(120))
    location = db.Column(db.String(140))
    description = db.Column(db.Text)
    image_file = db.Column(db.String(200))  # uploaded filename
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    reviews = db.relationship("Review", backref="book", lazy="dynamic", cascade="all,delete")
    wishlist = db.relationship("Wishlist", backref="book", lazy="dynamic", cascade="all,delete")

    def avg_rating(self):
        vals = [r.rating for r in self.reviews]
        return round(sum(vals) / len(vals), 2) if vals else 0


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # 1–5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)


class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)


class BuyRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(260), nullable=False)
    author = db.Column(db.String(200))
    details = db.Column(db.Text)
    budget = db.Column(db.Numeric(10, 2))
    is_free = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(140))
    image_file = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="buy_requests")  # This is enough


class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    message = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
