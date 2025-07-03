import streamlit as st
import sqlite3
from datetime import datetime
from nltk.sentiment import SentimentIntensityAnalyzer
import plotly.express as px

class Journal():

    # To be honest, this feels wrong to have this code pass
    def __init__(self):
        pass

    """ Since this program uses sqlite as a database. You have to create your own sqlite database. make sure that your sqlite table contains this following columns:
            id - integer, auto-increment, primary key
            date - text
            journal - text"""
    def add_journal(self, get_timestamp, get_diary):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()

            #Always specify the column names in your INSERT statement when not providing all columns, especially when using auto-increment primary keys.

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

    """ There is some errors into this, a small minor issue and that is if you are going to delete an entry. You have to press it twice so that it will change. I've tried adding experimental rerun() into this to fix it. But streamlit produces an error saying that there no such thing as that function (my streamlit is up-to-date btw.)"""
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
    

def Frontend():

    current_time = datetime.now().strftime("%m-%d %H:%M")

    st.markdown(
    "<div style='text-align: center;'>"
    "<h1>Coding Journal</h1>"
    "</div>",
    unsafe_allow_html=True)

    diary = st.text_area("Enter your journal entry here:")

    if "journal" not in st.session_state:
        st.session_state.journal = Journal()

    if "view_mode" not in st.session_state:
        st.session_state.view_mode = False


    add_clicked = st.button("Add Entry")
    
    if add_clicked:
        st.session_state.journal.add_journal(current_time, diary)
        st.success("Entry Added")
        st.session_state.view_mode = False

    view_clicked = st.button("View Entry")
    if view_clicked:
        st.session_state.view_mode = True

    if st.session_state.view_mode:
        journal_entries = st.session_state.journal.view_journal()
        if journal_entries:
            for index, journal_entry in enumerate(journal_entries, start=1):
                id = journal_entry[0]

                st.markdown(f"<h3>Day {index}:</h3>", unsafe_allow_html=True)
                st.markdown(f"<b>{journal_entry[1]}:</b>", unsafe_allow_html=True)
                st.write(f"{journal_entry[2]}")
                
                delete_clicked = st.button("Delete", key=f"delete_{id}")

                if delete_clicked:
                    st.session_state.journal.delete_journal(id)

        else:
            st.write("No entries found")

    graph_clicked = st.button("Analyze your Journal?")
    if graph_clicked:
        st.markdown(
        "<div style='text-align: center;'>"
        "<h1>Graphing</h1>"
        "</div>",
        unsafe_allow_html=True)

        st.session_state.journal.graphing()


if __name__ == "__main__":
    Frontend()
