from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, current_user, login_required, logout_user
import smtplib
import random
import os

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
        email = request.form.get("email", "")
        username = request.form.get("username", "")
        password1 = request.form.get("password1", "")
        password2 = request.form.get("password2", "")

        email_exist = User.query.filter_by(email=email).first()
        username_exist = User.query.filter_by(username=username).first()

        if email_exist:
            flash("Email already exist", category="error")
        elif username_exist:
            flash(f"{username} is already in use", category="error")
        elif password1 != password2:
            flash("Password doesn't match", category="error")
        elif not password1 or not password2:
            flash("Password fields cannot be empty", category="error")
        elif len(username) < 4:
            flash("Username must be at least five characters long", category="error")
        elif len(password1) < 8:
            flash("Password must be at least eight characters long", category="error")
        else:
            session["email"] = email
            session["username"] = username
            session["password"] = password2

            random_code = random.randint(100000, 999999)
            sender_email = os.getenv("EMAIL")

            subject = "Code Verification for CodingJourn"
            message = f"Thanks for logging in on my website. Your verification code is {random_code}"

            text = f"Subject: {subject}\n\n{message}"

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()

            server.login(sender_email, "bphe trqd tprv jvbm")
            server.sendmail(sender_email, email, text)

            session["code"] = random_code

            print(f"The first print {session['code']}")

            return redirect(url_for("auth.user_verify"))

    return render_template("sign-up.html", user=current_user)

@auth.route("/verify", methods=["GET", "POST"])
def user_verify():
    receiver_email = session["email"]

    if "email" in session:
        code = session["code"]

        if request.method == "POST":
            get_user_code = request.form.get("verification")

            print(f"The second print {code}")

            if int(get_user_code) == code:
                receiver_email = session["email"]
                receiver_password = session["password"]
                receiver_username = session["username"]

                new_user = User(email=receiver_email,
                                username=receiver_username,
                                password=generate_password_hash(receiver_password, method="pbkdf2:sha256"))
                db.session.add(new_user)
                db.session.commit()

                login_user(new_user, remember=True)
                flash("User is created", category="success")
                return redirect(url_for("views.home"))

            else:
                flash("Incorrect code input", category="error")

    return render_template("verify.html", email=receiver_email)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))