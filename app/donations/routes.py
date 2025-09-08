from flask import render_template, flash, redirect, url_for
from . import donations_bp
from app.forms import DonationForm
from app import db
from app.models import Donation
from flask_login import current_user

@donations_bp.route("/", methods=["GET","POST"])
def donate():
    form = DonationForm()
    if form.validate_on_submit():
        d = Donation(amount=form.amount.data, message=form.message.data.strip() if form.message.data else None, user_id=current_user.id if current_user.is_authenticated else None)
        db.session.add(d)
        db.session.commit()
        flash("Thank you! Your donation is recorded.", "success")
        # integrate payment gateway here
        return redirect(url_for("main.index"))
    return render_template("donations/donate.html", form=form)
