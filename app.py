
import streamlit as st

from chat import (
    ask_question,
    generate_quiz,
    generate_flashcards,
    generate_summary
)


# Page Config


st.set_page_config(
    page_title="Smart Study Bot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Smart Study Bot")


# Sidebar


st.sidebar.header("Settings")

model_choice = st.sidebar.selectbox(
    "Choose Model",
    ["Ollama", "Gemini"]
)

show_rewritten_query = st.sidebar.checkbox(
    "Show Rewritten Query",
    value=False
)

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:
    st.sidebar.success(
        f"Uploaded: {uploaded_file.name}"
    )

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()


# Session State


if "messages" not in st.session_state:
    st.session_state.messages = []


# Tabs


tab1, tab2, tab3, tab4 = st.tabs(
    [
        "💬 Ask Questions",
        "📝 Quiz",
        "🗂 Flashcards",
        "📖 Summary"
    ]
)


# TAB 1 - CHAT


with tab1:

    st.subheader("💬 Chat With Your Notes")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])

            if (
                message["role"] == "assistant"
                and "sources" in message
            ):

                with st.expander("📄 Sources"):

                    for source in message["sources"]:
                        st.write(f"• {source}")

    query = st.chat_input(
        "Ask a question..."
    )

    if query:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": query
            }
        )

        with st.chat_message("user"):
            st.write(query)

        with st.spinner("Thinking..."):

            result = ask_question(
                query,
                model_choice.lower()
            )

        answer = result["answer"]

        unique_sources = list(
            set(result["sources"])
        )

        with st.chat_message("assistant"):

            st.write(answer)

            if show_rewritten_query:

                st.caption(
                    f"🔍 Rewritten Query: "
                    f"{result['rewritten_query']}"
                )

            if unique_sources:

                with st.expander(
                    "📄 Sources"
                ):

                    for source in unique_sources:
                        st.write(
                            f"• {source}"
                        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": unique_sources
            }
        )


# TAB 2 - QUIZ


with tab2:

    st.subheader(
        "📝 Generate Quiz"
    )

    quiz_topic = st.text_input(
        "Enter Topic for Quiz"
    )

    if st.button(
        "Generate Quiz"
    ):

        if quiz_topic:

            with st.spinner(
                "Generating Quiz..."
            ):

                result = generate_quiz(
                    quiz_topic,
                    model_choice.lower()
                )

            st.markdown(
                result["quiz"]
            )

            if result.get("sources"):

                with st.expander(
                    "📄 Sources"
                ):

                    for source in result["sources"]:
                        st.write(
                            f"• {source}"
                        )


# TAB 3 - FLASHCARDS


with tab3:

    st.subheader(
        "🗂 Generate Flashcards"
    )

    flashcard_topic = st.text_input(
        "Enter Topic for Flashcards"
    )

    if st.button(
        "Generate Flashcards"
    ):

        if flashcard_topic:

            with st.spinner(
                "Generating Flashcards..."
            ):

                result = generate_flashcards(
                    flashcard_topic,
                    model_choice.lower()
                )
            st.write(result)

            st.markdown(
                result.get(
                    "flashcards",
                    "No flashcards generated"
            )
            )

            if result.get("sources"):

                with st.expander(
                    "📄 Sources"
                ):

                    for source in result["sources"]:
                        st.write(
                            f"• {source}"
                        )


# TAB 4 - SUMMARY


with tab4:

    st.subheader(
        "📖 Generate Study Guide"
    )

    summary_topic = st.text_input(
        "Enter Topic for Summary"
    )

    if st.button(
        "Generate Summary"
    ):

        if summary_topic:

            with st.spinner(
                "Generating Summary..."
            ):

                result = generate_summary(
                    summary_topic,
                    model_choice.lower()
                )

            st.write(result)

            st.markdown(
                result.get("summary",
                           "No summary generated"
                )
            )

            if result.get("sources"):

                with st.expander(
                    "📄 Sources"
                ):

                    for source in result["sources"]:
                        st.write(
                            f"• {source}"
                        )

