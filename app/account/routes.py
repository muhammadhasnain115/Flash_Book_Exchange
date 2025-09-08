from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import Book, Wishlist  
from app.forms import EditProfileForm  # FOR EDITING PROFILE
from app.forms import ChangePasswordForm  # FOR EDITING PROFILE


bp = Blueprint("account", __name__, url_prefix="/account")

UPLOAD_FOLDER = "app/static/uploads/avatars"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@bp.route("/my_listings")
@login_required
def my_listings():
    listings = current_user.listings.all()
    requests = current_user.buy_requests  # or .all() if needed
    return render_template("account/my_listings.html", listings=listings, requests=requests)

# Small API to toggle active status (used by JS)
@bp.route("/listing/toggle-active/<int:book_id>", methods=["POST"])
@login_required
def toggle_active(book_id):
    b = Book.query.get_or_404(book_id)
    if b.owner_id != current_user.id:
        abort(403)
    b.is_active = not b.is_active
    db.session.commit()
    return jsonify({"status": "ok", "is_active": b.is_active})

@bp.route("/listing/mark-sold/<int:book_id>", methods=["POST"])
@login_required
def mark_sold(book_id):
    b = Book.query.get_or_404(book_id)
    if b.owner_id != current_user.id:
        abort(403)
    b.is_sold = True
    b.is_gift = False
    db.session.commit()
    return jsonify({"status": "ok", "is_sold": True})

@bp.route("/listing/mark-gift/<int:book_id>", methods=["POST"])
@login_required
def mark_gift(book_id):
    b = Book.query.get_or_404(book_id)
    if b.owner_id != current_user.id:
        abort(403)
    b.is_gift = True
    b.is_sold = False
    db.session.commit()
    return jsonify({"status": "ok", "is_gift": True})

@bp.route("/listing/delete/<int:book_id>", methods=["POST"])
@login_required
def delete_listing(book_id):
    b = Book.query.get_or_404(book_id)
    if b.owner_id != current_user.id:
        abort(403)
    db.session.delete(b)
    db.session.commit()
    return jsonify({"status": "ok"})

@bp.route("/notifications")
@login_required
def notifications():
    # Placeholder page for now
    return render_template("account/notifications.html")

@bp.route("/profile")
@login_required
def profile():
    # Placeholder page for now
    return render_template("account/profile.html")

@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)  # prefill with current values

    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("account.profile"))

    return render_template("account/edit_profile.html", form=form)


@bp.route("/upload_avatar", methods=["POST"])
@login_required
def upload_avatar():
    if "avatar" not in request.files:
        flash("No file part", "danger")
        return redirect(url_for("account.profile"))

    file = request.files["avatar"]
    if file.filename == "":
        flash("No selected file", "danger")
        return redirect(url_for("account.profile"))

    if file:
        # create avatars folder inside /static if not exists
        upload_path = os.path.join(current_app.static_folder, "avatars")
        os.makedirs(upload_path, exist_ok=True)

        filename = f"user_{current_user.id}_{file.filename}"
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)

        # save filename in DB
        current_user.avatar_file = filename
        db.session.commit()

        flash("Avatar uploaded successfully!", "success")
    return redirect(url_for("account.profile"))

@bp.route("/remove_avatar")
@login_required
def remove_avatar():
    if current_user.avatar_file:
        # path to file
        file_path = os.path.join(current_app.static_folder, "avatars", current_user.avatar_file)
        if os.path.exists(file_path):
            os.remove(file_path)

        # clear from DB
        current_user.avatar_file = None
        db.session.commit()

        flash("Avatar removed successfully!", "success")
    else:
        flash("No avatar to remove.", "warning")

    return redirect(url_for("account.profile"))

@bp.route('/account/update_pass', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # Check if current password matches
        if not check_password_hash(current_user.password_hash, form.current_password.data):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for("account.change_password"))

        current_user.password_hash = generate_password_hash(form.new_password.data)

        db.session.commit()
        flash("✅ Password updated successfully!", "success")
        return redirect(url_for('account.edit_profile'))

    return render_template('account/update_pass.html', form=form)

    
@bp.route("/wishlist")
@login_required
def wishlist():
    """Show all books in current user's wishlist"""
    items = (
        db.session.query(Book)
        .join(Wishlist, Wishlist.book_id == Book.id)
        .filter(Wishlist.user_id == current_user.id)
        .all()
    )
    return render_template("account/wishlist.html", items=items)


@bp.route("/toggle-wishlist/<int:book_id>", methods=["POST"])
@login_required
def toggle_wishlist(book_id):
    """Add/remove a book from wishlist"""
    book = Book.query.get_or_404(book_id)
    existing = Wishlist.query.filter_by(user_id=current_user.id, book_id=book.id).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash(f"Removed '{book.title}' from your wishlist.", "info")
    else:
        new_item = Wishlist(user_id=current_user.id, book_id=book.id)
        db.session.add(new_item)
        db.session.commit()
        flash(f"Added '{book.title}' to your wishlist!", "success")

    return redirect(request.referrer or url_for("account.wishlist"))