import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import streamlit as st
from src.chatbot import Chatbot

if __name__ == "__main__":
    #initialize_vector_db()

    chatbot = Chatbot()
    chatbot.chat()
