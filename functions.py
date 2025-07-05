import streamlit as st
import sqlite3
from nltk.sentiment import SentimentIntensityAnalyzer
import plotly.express as px
import os


DB_PATH = "database.db"

if not os.path.exists(DB_PATH):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE diaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                journal TEXT
            )
        """)
        conn.commit()

class Journal():

    # To be honest, this feels wrong to have this code pass
    def __init__(self):
        pass

    def add_journal(self, get_timestamp, get_diary):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()

            cursor.execute("INSERT INTO diaries (date, journal) VALUES (?, ?)", (get_timestamp, get_diary))
            conn.commit()

    def view_journal(self):
        st.markdown(
        "<div style='text-align: center;'>"
        "<h3>Journal Entry</h3>"
        "</div>",
        unsafe_allow_html=True)

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM diaries")
            result = cursor.fetchall()
            return result

    def delete_journal(self, get_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM diaries WHERE id = ?", (get_id,))
            conn.commit()

    def graphing(self):

        analyzer = SentimentIntensityAnalyzer()
        date_list = []
        diary_list = []

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT date, journal FROM diaries")
            result = cursor.fetchall()

            for data in result:
                scores = analyzer.polarity_scores(data[1])
                overall_score = scores["compound"]

                date_list.append(data[0])
                diary_list.append(overall_score)

            figure = px.line(x=date_list, y=diary_list, labels={"x" : "Dates", "y" : "Scores"})
            st.plotly_chart(figure)

            return figure