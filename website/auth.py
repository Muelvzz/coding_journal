from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, current_user, login_required, logout_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        email_exist = User.query.filter_by(email=email).first()

        if email_exist:
            if check_password_hash(email_exist.password, password):
                flash("Logged in", category="success")
                login_user(email_exist, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password", category="error")
        else:
            flash("Email does not exist", category="error")        

    return render_template("login.html")

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exist = User.query.filter_by(email=email).first()
        username_exist = User.query.filter_by(username=username).first()

        if email_exist:
            flash("Email already exist", category="error")
        elif username_exist:
            flash(f"{username} is already in use", category="error")
        if password1 != password2:
            flash("Password doesn't match", category="error")

        elif len(username) < 4:
            flash("Username is too short", category="error")
        elif len(password1) < 8:
            flash("Password is too short", category="error")
        else:
            new_user = User(email=email,
                            username=username,
                            password=generate_password_hash(password2, method="pbkdf2:sha256"))
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash("User is created", category="success")

            return redirect(url_for("views.home"))

    return render_template("sign-up.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))