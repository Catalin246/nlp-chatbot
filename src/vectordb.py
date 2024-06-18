import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class VectorDB:
    def __init__(self, db_path='data/processed/vectordb.json'):
        self.db_path = db_path
        self.data = []
        self.load()

    # Add an item to the database.
    def add_item(self, text, vector):
        self.data.append({'text': text, 'vector': vector.tolist()})
        self.save()

    # Save the database to a file.
    def save(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.data, f)

    # Load the database from a file.
    def load(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                self.data = json.load(f)

    # Query the database for the top n most similar items.
    def query(self, vector, top_n=5):
        vectors = np.array([item['vector'] for item in self.data])
        similarities = cosine_similarity([vector], vectors)[0]
        top_indices = similarities.argsort()[-top_n:][::-1]
        return [self.data[idx] for idx in top_indices]
