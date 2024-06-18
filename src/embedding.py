from sentence_transformers import SentenceTransformer

class Embedding:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # Initialize the embedding model with the specified pre-trained model
        self.model = SentenceTransformer(model_name)

    def embed(self, text):
        # Embed the given text into a vector
        # If the input is a single string, convert it to a list
        if isinstance(text, str):
            text = [text]
        # Generate embeddings for the text
        embeddings = self.model.encode(text)
        return embeddings
