import streamlit as st
from datetime import datetime
from functions import Journal

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
                    
                delete_clicked = st.button("Delete", key=f"delete_{index}")

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
