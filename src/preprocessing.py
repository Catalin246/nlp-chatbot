import fitz  
import nltk
from nltk.tokenize import sent_tokenize
import re
import os
from embedding import Embedding
from vectordb import VectorDB

nltk.download('punkt')

class OERPreprocessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.embedder = Embedding()  
        self.vectordb = VectorDB()  

    def extract_text_from_pdf(self):
        """Extract text from the PDF file."""
        text = ""
        try:
            document = fitz.open(self.file_path)
            for page_num in range(document.page_count):
                page = document.load_page(page_num)
                text += page.get_text()
        except Exception as e:
            print(f"Error reading PDF file: {e}")
        return text

    def clean_text(self, text):
        """Clean the extracted text."""
        text = re.sub(r'\s+', ' ', text)  
        text = text.replace('\n', ' ')  
        text = re.sub(r'[^A-Za-z0-9\s.,;!?]', '', text)  
        return text.strip()

    def tokenize_text(self, text):
        """Tokenize the text into sentences."""
        return sent_tokenize(text)

    def chunk_text(self, sentences, chunk_size=400):
        """Chunk the text into smaller parts."""
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence.split())
            if current_length + sentence_length <= chunk_size:
                current_chunk.append(sentence)
                current_length += sentence_length
            else:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_length = sentence_length
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

    def preprocess(self, output_file=None):
        """Preprocess the OER file and optionally save the output to a file."""
        text = self.extract_text_from_pdf()
        cleaned_text = self.clean_text(text)
        sentences = self.tokenize_text(cleaned_text)
        chunks = self.chunk_text(sentences)
        
        embeddings = [self.embedder.embed(chunk) for chunk in chunks]  

        for chunk, embedding in zip(chunks, embeddings):
            self.vectordb.add_item(chunk, embedding[0]) 

        if output_file:
            with open(output_file, 'w') as f:
                for i, chunk in enumerate(chunks):
                    f.write(f"Chunk {i+1}:\n")
                    f.write(chunk + "\n\n")
        
        return chunks, embeddings

if __name__ == "__main__":
    file_paths = [
        "data/raw/b-information-technology-ter-2023-2024.pdf",
        "data/raw/b-technische-informatica-oer-2023-2024.pdf"
    ]
    
    for file_path in file_paths:
        output_file = os.path.join("data/processed", os.path.basename(file_path).replace('.pdf', '_chunks.txt'))
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        preprocessor = OERPreprocessor(file_path)
        chunks, embeddings = preprocessor.preprocess(output_file)

        print(f"Processed {file_path}, results saved to {output_file}")
