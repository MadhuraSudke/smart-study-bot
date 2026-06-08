import streamlit as st
from chat import ask_question

st.title("Smart Study Bot")

query = st.text_input("Ask a question")

if st.button("Submit"):

    result = ask_question(query)

    st.write("### Answer")
    st.write(result["answer"])

    st.write("### Sources")

    for source in result["sources"]:
        st.write(source)