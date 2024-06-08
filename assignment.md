# Final Assignment NLP

Create a chatbot that can answer questions about the assigned OER data.

The client for this assignment will be IVT and their wishes for the chatbot can be found in `ontwerpeisen.docx` and should be considered as the guidelines that will satisify the client. The rest of this documents add the technical requirements that will be used to grade your group on.

The chatbot should use the modern approach of using a Large language model (LLM) and Retrieval augmented Generation (RAG) to access data based on your assigned OER data.

The chat component can be handled mainly by a LLM hosted via ollama on your local machine. as for the retrieval part, you will focus on building the RAG component yourselfs.

## Requirements

- [ ] Preprocessing of OER files: Preprocess the assigned OER files (in whatever format they come in).
        This might involve cleaning, tokenizing, or converting them into a usable form.
        Chunking them into parts: Chunk the preprocessed OER data into smaller, more manageable pieces that can be used as building blocks for generating text.
        There are multiple years with multiple 
- [ ] Create a Embedding class (can be a implementation from a MTEB leaderboard)
        Embed given text to a vector that can be used for similarity matching.
- [ ] Creating a VectorDB class from scratch:
        Stores items with a vector and a text component: Create a VectorDB class that stores each chunked piece of OER data along with its corresponding vector representation.
        Allows the lookup of a top n amount of related texts based on their vector similarity.
        Persists data, so the database should not be recreated each time you start the application.
        You are allowed to add additional properties and functionalities to the VectorDB to accomadate your solution.
- [ ] Chatbot component:
        Use a Streamlit interface to create a user-friendly chat window (no points are awarded for customization; simply having a back-and-forth conversation is enough, and you can use existing Streamlit examples as a starting point).
        The chatbot should be able to understand and respond to user input in the form of natural language questions, this might require a bit of preprocessing.
        To generate responses, the chatbot will use a combination of LLMs (Large Language Models) and RAG (Retrieval augmented Generation).
        Build the chat component using an ollama LLM model (e.g. llama3 or phi3, or for those with less performant machines you can use a model like qwen).
        The chat flow should start with some questions about the student like what year and which OER is relevant for them.
        You are allowed to add some trigger words, that change the flow of the conversation (like reset).
        This component will also be graded based on the requirements within the `ontwerpeisen.docx`.

Scores are based on the following table

| Letter  | Explanation | Score |
|---|---|---|
| U |  Unsatisfactory | 20  |
| D |  Doubtful       | 40  |
| S |  Satisfactory   | 60  |
| G |  Good           | 80  |
| E |  Excellent      | 100 |

For all components code quality, will be taken into account. I suggest adding comments to make the code explainable, please also explain what does not work. I advise introducing unit tests, but this will be a minimal consideration for your grade, but it prevents you from writing monolitic functionalities that become a big ball of mud. The main focus is on the NLP components.

⚠️ It is important to only use offline (locally hosted) models when handling the OER data, as these are internal files for Inholland and should therefore not be leaked to external companies like OpenAI. This assignment should therefore also not use any form of external connection to copilot or chatGPT.

## Submission Guidelines

Provide a zip file containing your code, including preprocessing scripts, Embedding and VectorDB classes, LLM model, and Streamlit interface. I expect the file to be structered as follows

```
nlp_group_<number>.zip
    - README.md
    - data (could be used to store the VectorDB files and raw unpreprocessed data)
    - src (containing all python code)
    - requirements.txt
    - app.py
```

to test the program I should only have to run `python -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/streamlit run app.py` or its windows equivalent `python -m venv .venv && .venv\Scripts\pip.exe install -r requirements.txt && .venv\Scripts\streamlit run app.py` 

Include a README file with instructions on how to the chatbot works, and how to run the run the preprocessing steps for the OER files.

Have it start with the following text:

```
# NLP Chatbot 

group: <group number>
delivery data: %Y%m%dT%H%M%SZ
Members:
- Student 1 (123456)
- Student 2 (246824)
- Student 3 (321123)
- <student name> (<student number>)

## Introduction

## Code stucture


```

## Resources

Following the lectures & existing programming knowledge should be enough to be able to finish the assignment, but it is advised to find more resource regarding the creation of such a chatbot, to get you started these are some useful links related to the requirements.

https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps#build-a-chatgpt-like-app
https://ollama.com/blog/openai-compatibility

Please let me know if you have any questions or concerns about this assignment!