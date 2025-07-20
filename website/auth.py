from flask import Flask, render_template, Blueprint

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/sign-up")
def sign_up():
    pass