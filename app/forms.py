from flask_wtf import FlaskForm

from wtforms import (
    StringField, PasswordField, SubmitField, TextAreaField,
    BooleanField, DecimalField, SelectField
)
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange
from flask_wtf.file import FileField, FileAllowed

class SignupForm(FlaskForm):
    name = StringField("Full name", validators=[DataRequired(), Length(min=2, max=140)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=140)])
    phone = StringField("Phone number", validators=[DataRequired(), Length(min=6, max=32)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Create account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")


class BookForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=260)])
    author = StringField("Author", validators=[Optional(), Length(max=200)])
    condition = SelectField("Condition", choices=[("new", "New"), ("used", "Used")], validators=[DataRequired()])
    is_free = BooleanField("Mark as free")
    price = DecimalField("Price (PKR)", validators=[Optional(), NumberRange(min=0)], places=2)
    category = StringField("Category", validators=[Optional(), Length(max=120)])
    location = StringField("Location", validators=[Optional(), Length(max=140)])
    image = FileField("Upload Image", validators=[Optional(), FileAllowed(["jpg", "jpeg", "png", "gif"])])
    description = TextAreaField("Description", validators=[Optional(), Length(max=4000)])
    submit = SubmitField("Publish")


class ReviewForm(FlaskForm):
    rating = SelectField("Rating", choices=[(str(i), str(i)) for i in range(1, 6)], validators=[DataRequired()])
    comment = TextAreaField("Comment", validators=[Optional(), Length(max=2000)])
    submit = SubmitField("Submit Review")


class BuyRequestForm(FlaskForm):
    title = StringField("Book title", validators=[DataRequired(), Length(max=260)])
    author = StringField("Author", validators=[Optional(), Length(max=200)])
    details = TextAreaField("Details", validators=[Optional(), Length(max=2000)])
    is_free = BooleanField("Want for free")  # ✅ new field
    budget = DecimalField("Budget (PKR)", validators=[Optional(), NumberRange(min=0)], places=2)
    location = StringField("Location", validators=[Optional(), Length(max=140)])
    image = FileField("Upload Image", validators=[Optional(), FileAllowed(["jpg", "jpeg", "png", "gif"])])  # ✅ new field
    submit = SubmitField("Post Request")



class DonationForm(FlaskForm):
    amount = DecimalField("Amount (PKR)", validators=[DataRequired(), NumberRange(min=1)], places=2)
    message = StringField("Message (optional)", validators=[Optional(), Length(max=400)])
    submit = SubmitField("Donate")

class EditProfileForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=140)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=140)])
    phone = StringField("Phone", validators=[DataRequired(), Length(max=32)])
    submit = SubmitField("Save changes")

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField(
        'New Password',
        validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters long")]
    )
    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[DataRequired(), EqualTo('new_password', message="Passwords must match")]
    )
    submit = SubmitField('Update Password')