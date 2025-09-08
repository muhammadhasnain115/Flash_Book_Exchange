from flask import render_template, redirect, url_for, flash, request
from . import auth_bp
from app import db
from app.models import User
from app.forms import SignupForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required

@auth_bp.route("/signup", methods=["GET","POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered. Try logging in.", "warning")
            return redirect(url_for("auth.login"))
        user = User(name=form.name.data.strip(), email=form.email.data.lower().strip(), phone=form.phone.data.strip())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Welcome — your account is created.", "success")
        return redirect(url_for("main.index"))
    return render_template("auth/signup.html", form=form)



@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.index"))
        flash("Invalid credentials.", "danger")
    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("main.index"))
