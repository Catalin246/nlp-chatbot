import asyncio
import streamlit as st

class StreamlitUI:
    def __init__(self, chatbot):
        self.chatbot = chatbot

    def chat(self):
        """
        Launch the chatbot interface using Streamlit.
        """
        st.title("NLP Inholland Chatbot")

        # Language selection
        language = st.selectbox("Select Language / Selecteer taal", ("English", "Nederlands"))

        if "history" not in st.session_state:
            st.session_state.history = []

        if "user_input" not in st.session_state:
            st.session_state.user_input = ""

        # Set labels based on language
        if language == "Nederlands":
            year_label = "In welk jaar zit je?"
            oer_label = "Welke OER is relevant voor jou?"
            input_label = "Jij:"
        else:
            year_label = "What year are you in?"
            oer_label = "Which OER is relevant for you?"
            input_label = "You:"

        if not self.chatbot.student_info["year"]:
            st.session_state.user_input = st.text_input(year_label, key="year_input")
            if st.session_state.user_input:
                self.chatbot.student_info["year"] = st.session_state.user_input
                st.session_state.user_input = ""

        if self.chatbot.student_info["year"] and not self.chatbot.student_info["oer"]:
            st.session_state.user_input = st.text_input(oer_label, key="oer_input")
            if st.session_state.user_input:
                self.chatbot.student_info["oer"] = st.session_state.user_input
                st.session_state.user_input = ""

        if self.chatbot.student_info["year"] and self.chatbot.student_info["oer"]:
            for chat in st.session_state.history:
                st.write(f"Jij: {chat['user']}" if language == "Nederlands" else f"You: {chat['user']}")
                st.write(f"Bot: {chat['bot']}")

            async def submit_data():
                """
                Submit the user input and get a response from the chatbot.
                """
                if st.session_state.user_input:
                    if language == "Nederlands":
                        response = await self.chatbot.get_response(st.session_state.user_input, lang="nl")
                    else:
                        response = await self.chatbot.get_response(st.session_state.user_input, lang="en")
                    st.session_state.history.append({"user": st.session_state.user_input, "bot": response})
                    st.session_state.user_input = ""

            st.text_input(input_label, key="user_input", on_change=lambda: asyncio.run(submit_data()))
