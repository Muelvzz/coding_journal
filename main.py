import streamlit as st
import sqlite3
from datetime import datetime

class Journal():
    def __init__(self):
        self.connection = sqlite3.connect("database.db")

    def add_journal(self, get_timestamp, get_diary):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Diary VALUES (?,?)", (get_timestamp, get_diary))
            conn.commit()

    def view_journal(self):
        st.markdown(
        "<div style='text-align: center;'>"
        "<h3>Journal Entry</h3>"
        "</div>",
        unsafe_allow_html=True)

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Diary")
            result = cursor.fetchall()
            return result

    def delete_journal(self, index):
        if 0 <= index < len(self.journal_entries):
            deleted_entry = self.journal_entries.pop(index)
        else:
            st.write("Invalid entry index")
    

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

    l, r = st.columns(2)
    with l:
        add_clicked = st.button("Add Entry")
        
        if add_clicked:
            st.session_state.journal.add_journal(current_time, diary)
            st.success("Entry Added")

    with r:
        view_clicked = st.button("View Entry")

        if view_clicked:
            journal_entries = st.session_state.journal.view_journal()
            if journal_entries:
                for journal_entry in journal_entries:
                    st.write(f"{journal_entry[0]}: {journal_entry[1]}")
            else:
                st.write("No entries found")


if __name__ == "__main__":
    Frontend()
