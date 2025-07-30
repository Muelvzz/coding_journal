from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Journal
from . import db
from nltk.sentiment import SentimentIntensityAnalyzer
from rake_nltk import Rake

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
            rake = Rake()

            # Analyzing Journal Content
            score = analyzer.polarity_scores(content)
            analysis = score["compound"]

            # Identifying Keyword of Journal
            content = content.replace("(","").replace(")","")
            rake.extract_keywords_from_text(content)
            get_keywords = rake.get_ranked_phrases()
            sorted_keywords = set([keyword for keyword in get_keywords if len(keyword.split()) > 1])
            keywords = ", ".join(sorted_keywords)

            journal = Journal(content=content, title=title, author=current_user.id, analysis=analysis, keywords=keywords)
            db.session.add(journal)
            db.session.commit()

            return redirect(url_for("views.home"))

    return render_template("add_journal.html", user=current_user)

@views.route("/delete/<get_id>")
def delete_journal(get_id):

    journal = Journal.query.filter_by(id=get_id).first()

    db.session.delete(journal)
    db.session.commit()

    flash("Journal successfully deleted", category="success")

    return redirect(url_for("views.home"))

@views.route("update/<get_id>", methods=["POST", "GET"])
def update_journal(get_id):

    journal = Journal.query.filter_by(id=get_id).first()

    if request.method == "POST":
        update_title = request.form.get("update_text_title")
        update_text = request.form.get("update_text")

        journal.title = update_title
        journal.content = update_text

        db.session.commit()

        flash("Journal updated", category="success")

        return redirect(url_for("views.home"))
    
    return render_template("update_journ.html",
                            title=journal.title,
                            content=journal.content)

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