import streamlit as st
from embedding import Embedding
from vectordb import VectorDB
from langchain.llms import Ollama
import asyncio
from cachetools import TTLCache

class Chatbot:
    def __init__(self):
        """
        Initialize the Chatbot class.
        """
        self.conversation_history = []
        self.embedder = Embedding()
        self.vectordb = VectorDB()
        self.llm = Ollama(base_url='http://localhost:11434', model="llama3")
        self.student_info = {"year": None, "oer": None}
        self.cache = TTLCache(maxsize=100, ttl=300)  # Cache responses for 5 minutes

    def preprocess_input(self, user_input):
        """
        Preprocess the user input for better understanding.
        """
        return user_input.strip().lower()

    async def async_embed(self, user_input):
        """
        Asynchronous embedding of user input.
        """
        return self.embedder.embed(user_input)[0]

    async def async_query_vectordb(self, embedding):
        """
        Asynchronous query to the vector database.
        """
        return self.vectordb.query(embedding, top_n=1)

    async def get_response(self, user_input):
        """
        Get a response from the chatbot based on the user input.
        """
        user_input = self.preprocess_input(user_input)

        # Check cache
        if user_input in self.cache:
            return self.cache[user_input]

        if user_input == "reset":
            self.conversation_history = []
            return "Conversation reset."

        # Asynchronous embedding and querying
        user_embedding = await self.async_embed(user_input)
        results = await self.async_query_vectordb(user_embedding)

        if results:
            context = results[0]['text']
            try:
                response = self.llm(context + " " + user_input)
            except Exception as e:
                response = f"Failed to generate response using LLM: {e}"
        else:
            response = "I couldn't find any relevant information for your query. Please try again."

        # Update conversation history and cache
        self.conversation_history.append({"user": user_input, "bot": response})
        self.cache[user_input] = response

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

        if not self.student_info["year"]:
            st.session_state.user_input = st.text_input("What year are you in?", key="year_input")
            if st.session_state.user_input:
                self.student_info["year"] = st.session_state.user_input
                st.session_state.user_input = ""
        
        if self.student_info["year"] and not self.student_info["oer"]:
            st.session_state.user_input = st.text_input("Which OER is relevant for you?", key="oer_input")
            if st.session_state.user_input:
                self.student_info["oer"] = st.session_state.user_input
                st.session_state.user_input = ""

        if self.student_info["year"] and self.student_info["oer"]:
            for chat in st.session_state.history:
                st.write(f"You: {chat['user']}")
                st.write(f"Bot: {chat['bot']}")

            async def submit_data():
                """
                Submit the user input and get a response from the chatbot.
                """
                if st.session_state.user_input:
                    response = await self.get_response(st.session_state.user_input)
                    st.session_state.history.append({"user": st.session_state.user_input, "bot": response})
                    st.session_state.user_input = ""

            st.text_input("You:", key="user_input", on_change=lambda: asyncio.run(submit_data()))

