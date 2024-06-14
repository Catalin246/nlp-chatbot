import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class VectorDB:
    def __init__(self, db_path='data/processed/vectordb.json'):
        self.db_path = db_path
        self.data = []
        self.load()

    def add_item(self, text, vector):
        """
        Add an item to the database.
        """
        self.data.append({'text': text, 'vector': vector.tolist()})
        self.save()

    def save(self):
        """Save the database to a file."""
        with open(self.db_path, 'w') as f:
            json.dump(self.data, f)

    def load(self):
        """Load the database from a file."""
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                self.data = json.load(f)

    def query(self, vector, top_n=5):
        """
        Query the database for the top n most similar items.
        """
        vectors = np.array([item['vector'] for item in self.data])
        similarities = cosine_similarity([vector], vectors)[0]
        top_indices = similarities.argsort()[-top_n:][::-1]
        return [self.data[idx] for idx in top_indices]
