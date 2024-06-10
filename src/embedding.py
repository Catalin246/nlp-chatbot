from sentence_transformers import SentenceTransformer

class Embedding:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the embedding model.
        
        Parameters:
        model_name (str): The name of the pre-trained model from sentence-transformers.
        """
        self.model = SentenceTransformer(model_name)

    def embed(self, text):
        """
        Embed the given text into a vector.
        
        Parameters:
        text (str or list of str): The text to embed.
        
        Returns:
        numpy.ndarray: The embeddings of the given text.
        """
        if isinstance(text, str):
            text = [text]
        embeddings = self.model.encode(text)
        return embeddings
