import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from src.chatbot import Chatbot

class TestChatbot(unittest.TestCase):
    def setUp(self):
        self.chatbot = Chatbot()
        self.chatbot.embedder = MagicMock()
        self.chatbot.vectordb = MagicMock()
        self.chatbot.llm = MagicMock()

    @patch('src.chatbot.Chatbot.async_embed', new_callable=AsyncMock)
    @patch('src.chatbot.Chatbot.async_query_vectordb', new_callable=AsyncMock)
    async def test_get_response(self, mock_query_vectordb, mock_async_embed):
        # Mocking embedding and vector DB responses
        mock_async_embed.return_value = "mock_embedding"
        mock_query_vectordb.return_value = [{'text': 'mock_context'}]
        self.chatbot.llm.return_value = "mock_llm_response"
        
        response = await self.chatbot.get_response("Hello")
        self.assertEqual(response, "mock_llm_response")

    async def test_get_response_reset(self):
        response = await self.chatbot.get_response("reset")
        self.assertEqual(response, "Conversation reset.")
        self.assertEqual(self.chatbot.conversation_history, [])

    async def test_get_response_no_results(self):
        self.chatbot.async_embed = AsyncMock(return_value="mock_embedding")
        self.chatbot.async_query_vectordb = AsyncMock(return_value=[])
        
        response = await self.chatbot.get_response("Hello")
        self.assertEqual(response, "I couldn't find any relevant information for your query. Please try again.")

    async def test_get_response_cache(self):
        self.chatbot.cache["hello"] = "cached response"
        response = await self.chatbot.get_response("hello")
        self.assertEqual(response, "cached response")

if __name__ == '__main__':
    unittest.main()
