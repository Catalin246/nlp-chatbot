# NLP Inholland Chatbot 

group: 8
delivery date: 21/06/2024
Members:
- Student 1 "Avornicesei, Cătălin" <690325@student.inholland.nl>
- Student 2 "Paracchini, Roberta" <677676@student.inholland.nl>
- Student 3 "Noşca, Tudor" <678549@student.inholland.nl>
- Student 4 "Aouragh, Salah" <691096@student.inholland.nl>

## Introduction

This project is an NLP-based chatbot designed to answer questions about OER data using a combination of LLM and RAG techniques. 

## Code structure

- **data**: Contains raw and processed OER data.
- **src**: Contains all the source code including preprocessing, embedding, vector database, and chatbot functionalities.
- **requirements.txt**: Lists all the dependencies required for the project.
- **app.py**: The main entry point for the Streamlit application.

## How to Run the project with Linux

1. Create a virtual environment and install dependencies:
    ```bash
    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt
    ```

2. Preprocess the OER (Run the preprocessing script to prepare the OER. This step involves processing raw data into a format suitable for further analysis or model training. Note that this step only needs to be performed once.)
    ```bash
    python3 src/preprocessing.py
    ```

3. Run the Streamlit app:
    ```bash
    .venv/bin/streamlit run app.py
    ```

4. Run the tests
    ```bash
    python3 -m unittest discover -s .\src\tests\
    ```

## Preprocessing OER Files

The preprocessing script loads, cleans, tokenizes, and chunks the OER data. Run the preprocessing script to prepare the data before starting the chatbot.

## Embedding and VectorDB

The embedding class converts text into vector embeddings using a SentenceTransformer model. The VectorDB class stores these embeddings and provides a method for querying similar texts based on vector similarity.
