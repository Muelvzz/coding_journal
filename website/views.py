from flask import Flask, render_template, Blueprint
from flask_login import login_required

views = Blueprint("views", __name__)

@views.route("/")
@login_required
def home():
    return render_template("home.html")

@views.route("/add")
@login_required
def add_journal():
    return render_template("add_journal.html")

@views.route("/about")
def about():
    return render_template("about.html")