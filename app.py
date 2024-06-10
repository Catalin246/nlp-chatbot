import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import streamlit as st
from src.chatbot import Chatbot

if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.chat()
