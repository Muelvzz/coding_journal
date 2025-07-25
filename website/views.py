from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Journal
from . import db
from nltk.sentiment import SentimentIntensityAnalyzer

views = Blueprint("views", __name__)

@views.route("/")
@login_required
def home():

    journals = Journal.query.all()

    return render_template("home.html", user=current_user, journals=journals)

@views.route("/add", methods=["POST", "GET"])
@login_required
def add_journal():
    analyzer = SentimentIntensityAnalyzer()

    if request.method == "POST":
        title = request.form.get("text_title")
        content = request.form.get("text")

        if not title:
            flash("Your post lacks a title", category="error")

        elif not content:
            flash("Your post lacks a content", category="error")

        else:
            score = analyzer.polarity_scores(content)
            analysis = score["compound"]

            journal = Journal(content=content, title=title, author=current_user.id, analysis=analysis)
            db.session.add(journal)
            db.session.commit()

            return redirect(url_for("views.home"))

    return render_template("add_journal.html", user=current_user)

@views.route("/delete/<get_id>")
def delete_journal(get_id):

    journal = Journal.query.filter_by(id=get_id).first()

    db.session.delete(journal)
    db.session.commit()

    flash("Post successfully deleted", category="success")

    return redirect(url_for("views.home"))

@views.route("/journ/<get_username>")
@login_required
def load_user_journal(get_username):

    user = User.query.filter_by(username=get_username).first()
    journals = Journal.query.filter_by(author=user.id).all()

    journal_analysis = [data.analysis for data in journals]
    date_entries = [data.date_created.strftime(r"%Y-%m-%d") for data in journals]

    return render_template("journ.html",
                            user=current_user,
                            journals=journals,
                            username=user.username,
                            date_entries=date_entries,
                            journal_analysis=journal_analysis)

@views.route("/about")
def about():
    return render_template("about.html")