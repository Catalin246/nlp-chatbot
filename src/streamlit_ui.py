import asyncio
import streamlit as st
from src.chatbot import Chatbot

class StreamlitUI:
    def __init__(self, chatbot):
        self.chatbot = chatbot

    def chat(self):
        """
        Launch the chatbot interface using Streamlit.
        """
        st.title("NLP Inholland Chatbot")

        if "history" not in st.session_state:
            st.session_state.history = []

        if "user_input" not in st.session_state:
            st.session_state.user_input = ""

        if not self.chatbot.student_info["year"]:
            st.session_state.user_input = st.text_input("In welk jaar zit je?", key="year_input")
            if st.session_state.user_input:
                self.chatbot.student_info["year"] = st.session_state.user_input
                st.session_state.user_input = ""

        if self.chatbot.student_info["year"] and not self.chatbot.student_info["oer"]:
            st.session_state.user_input = st.text_input("Welke OER is voor jou relevant?", key="oer_input")
            if st.session_state.user_input:
                self.chatbot.student_info["oer"] = st.session_state.user_input
                st.session_state.user_input = ""

        if self.chatbot.student_info["year"] and self.chatbot.student_info["oer"]:
            for chat in st.session_state.history:
                st.write(f"Jij: {chat['user']}")
                st.write(f"Bot: {chat['bot']}")

            async def submit_data():
                """
                Submit the user input and get a response from the chatbot.
                """
                if st.session_state.user_input:
                    response = await self.chatbot.get_response(st.session_state.user_input)
                    st.session_state.history.append({"user": st.session_state.user_input, "bot": response})
                    st.session_state.user_input = ""

            st.text_input("Jij:", key="user_input", on_change=lambda: asyncio.run(submit_data()))
