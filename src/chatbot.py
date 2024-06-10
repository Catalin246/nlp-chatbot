import streamlit as st
from embedding import Embedding
from vectordb import VectorDB
from ollama import Client

class Chatbot:
    def __init__(self):
        """
        Initialize the Chatbot class.
        """
        self.conversation_history = []
        self.embedder = Embedding()
        self.vectordb = VectorDB()
        self.llm = Client() 
        # self.initial_questions = [
        #     "Hello! What year are you in?",
        #     "Which OER (Open Educational Resource) is relevant for you?"
        # ]
        self.current_question_index = 0

    def preprocess_input(self, user_input):
        """
        Preprocess the user input for better understanding.
        
        Parameters:
        user_input (str): The user's input message.
        
        Returns:
        str: The preprocessed input.
        """
        # Example preprocessing steps
        user_input = user_input.strip().lower()
        return user_input

    def get_response(self, user_input):
        """
        Get a response from the chatbot based on the user input.

        Parameters:
        user_input (str): The user's input message.

        Returns:
        str: The chatbot's response.
        """
        user_input = self.preprocess_input(user_input)

        # Check for reset trigger word
        if user_input == "reset":
            self.conversation_history = []
            self.current_question_index = 0
            return "Conversation reset. " + self.initial_questions[self.current_question_index]

        # If initial questions are not completed, ask them first
        if self.current_question_index < len(self.initial_questions):
            response = self.initial_questions[self.current_question_index]
            self.current_question_index += 1
        else:
            # Embed the user input
            user_embedding = self.embedder.embed(user_input)[0]
            
            # Query the vector database for the most similar text
            results = self.vectordb.query(user_embedding, top_n=1)
            
            # Generate a response based on the most similar text using LLM
            if results:
                context = results[0]['text']
                try:
                    if self.llm:
                        response = self.llm.generate(prompt=context + " " + user_input)  # Corrected method call
                    else:
                        response = "LLM is not available."
                except Exception as e:
                    response = f"Failed to generate response using LLM: {e}"
            else:
                response = "I couldn't find any relevant information for your query. Please try again."

        self.conversation_history.append({"user": user_input, "bot": response})
        return response

    def chat(self):
        """
        Launch the chatbot interface using Streamlit.
        """
        st.title("NLP Inholland Chatbot")

        if "history" not in st.session_state:
            st.session_state.history = []

        if "user_input" not in st.session_state:
            st.session_state.user_input = ""

        for chat in st.session_state.history:
            st.write(f"You: {chat['user']}")
            st.write(f"Bot: {chat['bot']}")

        def submit_data():
            """
            Submit the user input and get a response from the chatbot.
            """
            if st.session_state.user_input:
                response = self.get_response(st.session_state.user_input)
                st.session_state.history.append({"user": st.session_state.user_input, "bot": response})
                st.session_state.user_input = ""  

        st.text_input("You:", key="user_input", on_change=submit_data)
