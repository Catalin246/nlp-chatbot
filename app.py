import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.chatbot import Chatbot
from src.streamlit_ui import StreamlitUI

if __name__ == "__main__":
    chatbot = Chatbot()
    ui = StreamlitUI(chatbot)
    ui.chat()
