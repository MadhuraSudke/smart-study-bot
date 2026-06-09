import streamlit as st
from chat import ask_question

st.set_page_config(
page_title="Smart Study Bot",
page_icon="🤖"
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

if st.sidebar.button("🗑️ Clear Chat"):
  st.session_state.messages = []
  st.rerun()


# Chat History



if "messages" not in st.session_state:
  st.session_state.messages = []

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



# Chat Input

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

        with st.expander("📄 Sources"):

            for source in unique_sources:
                st.write(f"• {source}")

st.session_state.messages.append(
    {
        "role": "assistant",
        "content": answer,
        "sources": unique_sources
    }
)
with st.spinner("Thinking..."):
    result = ask_question(
        query,
        model_choice.lower()
    )

