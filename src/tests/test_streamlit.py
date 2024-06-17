import unittest
from unittest.mock import patch, AsyncMock
import streamlit as st
import asyncio
from src.chatbot import Chatbot
from src.streamlit_ui import StreamlitUI

class TestStreamlitUI(unittest.TestCase):
    def setUp(self):
        self.chatbot = Chatbot()
        self.ui = StreamlitUI(self.chatbot)

    @patch('streamlit.text_input')
    @patch('streamlit.title')
    @patch('streamlit.write')
    def test_initial_state(self, mock_write, mock_title, mock_text_input):
        # Reset the Streamlit session state
        st.session_state.clear()

        # Set up the mock for text input
        mock_text_input.return_value = ''

        # Run the chat method
        self.ui.chat()

        # Verify that the title is set correctly
        mock_title.assert_called_once_with("NLP Inholland Chatbot")

        # Verify that the initial text input for the year is created
        mock_text_input.assert_any_call("What year are you in?", key="year_input")

        # Verify that the text input for OER is not called yet
        with self.assertRaises(AssertionError):
            mock_text_input.assert_any_call("Which OER is relevant for you?", key="oer_input")

    @patch('streamlit.text_input')
    @patch('streamlit.title')
    @patch('streamlit.write')
    def test_collect_year_input(self, mock_write, mock_title, mock_text_input):
        # Reset the Streamlit session state
        st.session_state.clear()

        # Simulate entering year input
        st.session_state.user_input = '2023'
        self.chatbot.student_info["year"] = None

        # Set up the mock for text input
        mock_text_input.return_value = '2023'

        # Run the chat method
        self.ui.chat()

        # Verify that the year is set correctly
        self.assertEqual(self.chatbot.student_info["year"], '2023')

    @patch('streamlit.text_input')
    @patch('streamlit.title')
    @patch('streamlit.write')
    def test_collect_oer_input(self, mock_write, mock_title, mock_text_input):
        # Reset the Streamlit session state
        st.session_state.clear()

        # Simulate year is already entered
        self.chatbot.student_info["year"] = '2023'
        self.chatbot.student_info["oer"] = None

        # Set up the mock for text input
        mock_text_input.return_value = 'Sample OER'

        # Run the chat method
        self.ui.chat()

        # Verify that the OER text input is called
        mock_text_input.assert_any_call("Which OER is relevant for you?", key="oer_input")

        # Verify that the OER is set correctly
        self.assertEqual(self.chatbot.student_info["oer"], 'Sample OER')

    @patch('streamlit.text_input')
    @patch('streamlit.title')
    @patch('streamlit.write')
    @patch('asyncio.run')
    @patch('src.chatbot.Chatbot.get_response', new_callable=AsyncMock)
    def test_submit_data(self, mock_get_response, mock_async_run, mock_write, mock_title, mock_text_input):
        # Reset the Streamlit session state
        st.session_state.clear()

        # Simulate a chat history and user input
        st.session_state.history = []
        st.session_state.user_input = 'Hello'
        self.chatbot.student_info["year"] = '2023'
        self.chatbot.student_info["oer"] = 'Sample OER'

        # Set up the mock for text input
        mock_text_input.return_value = 'Hello'

        # Mock the get_response method
        mock_get_response.return_value = "mock_response"

        # Define an async test method
        async def async_test_method():
            # Define a helper function to submit data
            async def submit_data_helper():
                if st.session_state.user_input:
                    await self.ui.chat()  # This might need to be called directly if `ui.chat()` is an async method

            # Patch asyncio.run to run the submit_data coroutine
            async def mock_run(coro):
                return await coro
            
            mock_async_run.side_effect = mock_run

            # Run the chat method
            self.ui.chat()

            # Simulate the on_change callback
            await submit_data_helper()

            # Verify that the response is added to the history
            self.assertEqual(len(st.session_state.history), 1)
            self.assertEqual(st.session_state.history[0]['user'], 'Hello')
            self.assertEqual(st.session_state.history[0]['bot'], 'mock_response')

        # Run the async test method
        asyncio.run(async_test_method())

if __name__ == '__main__':
    unittest.main()
