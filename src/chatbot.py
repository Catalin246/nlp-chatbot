import streamlit as st

class Chatbot:
    def __init__(self):
        self.conversation_history = []

    def get_response(self, user_input):
        response = "Thank you for your question. At this model is not fully working so I cannot provide you a proper answer for your question. Have a nice day!"
        self.conversation_history.append({"user": user_input, "bot": response})
        return response

    def chat(self):
        st.title("Inholland Chatbot")

        if "history" not in st.session_state:
            st.session_state.history = []

        if "user_input" not in st.session_state:
            st.session_state.user_input = ""

        for chat in st.session_state.history:
            st.write(f"You: {chat['user']}")
            st.write(f"Bot: {chat['bot']}")

        def submit_data():
            if st.session_state.user_input:
                response = self.get_response(st.session_state.user_input)
                st.session_state.history.append({"user": st.session_state.user_input, "bot": response})
                st.session_state.user_input = ""  

        st.text_input("You:", key="user_input", on_change=submit_data)

