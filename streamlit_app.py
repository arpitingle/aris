import streamlit as st
from rag import ChatBot

st.set_page_config(page_title="AI Mentor ChatBot")

@st.cache_resource
def get_chatbot():
    return ChatBot()

def display_messages():
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message_type = "human" if is_user else "assistant"
        with st.chat_message(message_type):
            st.write(msg)

def process_input(user_input: str):
    st.session_state["messages"].append((user_input, True))
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state["assistant"].ask(user_input)
            st.write(response)
    st.session_state["messages"].append((response, False))

def main():
    st.title("AI Mentor ChatBot")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if "assistant" not in st.session_state:
        st.session_state["assistant"] = get_chatbot()

    display_messages()

    if user_input := st.chat_input("Type your message here..."):
        process_input(user_input)
        st.rerun()

    if st.button("Clear Chat History"):
        st.session_state["messages"] = []
        st.session_state["assistant"].clear()
        st.rerun()

if __name__ == "__main__":
    main()