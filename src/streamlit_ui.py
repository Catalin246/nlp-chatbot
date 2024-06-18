import asyncio
import streamlit as st

class StreamlitUI:
    def __init__(self, chatbot):
        # Initialize the StreamlitUI class with a chatbot instance.
        self.chatbot = chatbot

    # Launch the chatbot interface using Streamlit.
    def chat(self):
        st.title("NLP Inholland Chatbot")

        # Initialize language state if not already set.
        if "language" not in st.session_state:
            st.session_state.language = "English"

        # Language selection dropdown.
        language = st.selectbox("Select Language / Selecteer taal", ("English", "Nederlands"))

        # Clear history if the selected language changes.
        if language != st.session_state.language:
            st.session_state.language = language
            st.session_state.history = []

        # Initialize chat history if not already set.
        if "history" not in st.session_state:
            st.session_state.history = []

        # Initialize user input state if not already set.
        if "user_input" not in st.session_state:
            st.session_state.user_input = ""

        # Set labels based on the selected language.
        if language == "Nederlands":
            year_label = "In welk jaar zit je?"
            oer_label = "Welke OER is relevant voor jou?"
            input_label = "Jij:"
        else:
            year_label = "What year are you in?"
            oer_label = "Which OER is relevant for you?"
            input_label = "You:"

        # If the student's year information is not set, prompt the user to enter it.
        if not self.chatbot.student_info["year"]:
            st.session_state.user_input = st.text_input(year_label, key="year_input")
            if st.session_state.user_input:
                self.chatbot.student_info["year"] = st.session_state.user_input
                st.session_state.user_input = ""

        # If the student's year information is set but OER information is not, prompt the user to enter it.
        if self.chatbot.student_info["year"] and not self.chatbot.student_info["oer"]:
            st.session_state.user_input = st.text_input(oer_label, key="oer_input")
            if st.session_state.user_input:
                self.chatbot.student_info["oer"] = st.session_state.user_input
                st.session_state.user_input = ""

        # If both the student's year and OER information are set, display the chat history and input field.
        if self.chatbot.student_info["year"] and self.chatbot.student_info["oer"]:
            # Display chat history.
            for chat in st.session_state.history:
                st.write(f"Jij: {chat['user']}" if language == "Nederlands" else f"You: {chat['user']}")
                st.write(f"Bot: {chat['bot']}")

            # Asynchronous function to submit user input and get a response from the chatbot.
            async def submit_data():
                if st.session_state.user_input:
                    # Get response from the chatbot based on the selected language.
                    if language == "Nederlands":
                        response = await self.chatbot.get_response(st.session_state.user_input, lang="nl")
                    else:
                        response = await self.chatbot.get_response(st.session_state.user_input, lang="en")
                    
                    # Append the user input and chatbot response to the chat history.
                    st.session_state.history.append({"user": st.session_state.user_input, "bot": response})
                    st.session_state.user_input = ""

            # Input field for the user to enter their message, with on_change event to submit data.
            st.text_input(input_label, key="user_input", on_change=lambda: asyncio.run(submit_data()))
