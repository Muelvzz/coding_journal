import streamlit as st
from datetime import datetime

class Journal():
    def __init__(self):
        self.journal_entries = []

    def add_journal(self, get_timestamp, get_diary):
        entry = {"Timestamp" : get_timestamp, "Diary" : get_diary}
        self.journal_entries.append(entry)

    def view_journal(self):
        st.markdown(
        "<div style='text-align: center;'>"
        "<h3>Journal Entry</h3>"
        "</div>",
        unsafe_allow_html=True)

        for index, item in enumerate(self.journal_entries):
            timestamp = item["Timestamp"]
            diary = item["Diary"]

            st.write(f"{timestamp}: \n{diary}\n")
            st.button(f"Delete", key=f"delete_{index}", on_click=self.delete_journal, args=(index,))

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
            st.session_state.journal.view_journal()


if __name__ == "__main__":
    Frontend()
