# NLP Chatbot 

group: 8
delivery date: 
Members:
- Student 1 (123456)
- Student 2 (246824)
- Student 3 (321123)
- Student 4 (321123)

## Introduction

This project is an NLP-based chatbot designed to answer questions about OER data using a combination of LLM and RAG techniques. 

## Code structure

- **data**: Contains raw and processed OER data.
- **src**: Contains all the source code including preprocessing, embedding, vector database, and chatbot functionalities.
- **requirements.txt**: Lists all the dependencies required for the project.
- **app.py**: The main entry point for the Streamlit application.

## How to Run

1. Create a virtual environment and install dependencies:
    ```bash
    python -m venv .venv
    .venv/bin/pip install -r requirements.txt
    ```

2. Run the Streamlit app:
    ```bash
    .venv/bin/streamlit run app.py
    ```

## Preprocessing OER Files

The preprocessing script loads, cleans, tokenizes, and chunks the OER data. Run the preprocessing script to prepare the data before starting the chatbot.

## Embedding and VectorDB

The embedding class converts text into vector embeddings using a SentenceTransformer model. The VectorDB class stores these embeddings and provides a method for querying similar texts based on vector similarity.
