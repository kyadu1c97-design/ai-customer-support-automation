AI Customer Support Automation

Overview

This project is an AI-powered customer support automation system that answers user queries using PDF documents and FAQs. It uses a Retrieval-Augmented Generation (RAG) approach to deliver accurate, context-aware, and reliable responses.

---

Features

- Automates customer query handling
- Answers questions from PDF documents
- Supports FAQ-based queries
- Provides context-aware responses
- Applies strict filtering to reduce hallucinations
- Displays answer sources (PDF / FAQ)
- Interactive user interface using Streamlit

---

Tech Stack

- Backend: FastAPI
- Frontend: Streamlit
- LLM: Ollama (TinyLLaMA)
- Embeddings: Sentence Transformers
- Vector Database: FAISS
- Framework: LangChain

---

Project Structure

ai-customer-support-automation/
│── main.py
│── chatbot.py
│── vector_store.py
│── ui.py
│── data/
│   ├── sample.pdf
│   ├── faqs.txt
│── requirements.txt
│── README.md
│── .gitignore

---

How to Run the Project

1. Install Dependencies

pip install -r requirements.txt

2. Create Vector Database

python vector_store.py

3. Start Backend Server

uvicorn main:app --reload

4. Run Frontend UI

streamlit run ui.py

---

Ollama Setup

This project uses a local large language model through Ollama.

1. Install Ollama from: https://ollama.com
2. Run the model:
   ollama run tinyllama

Make sure Ollama is running before starting the chatbot.

---

API Endpoints

- GET / → API status
- GET /health → Health check
- POST /chat → Submit user query and get response

---

How It Works

1. Loads data from PDF and FAQ files
2. Splits the content into smaller chunks
3. Converts text into embeddings
4. Stores embeddings in FAISS vector database
5. Retrieves relevant context based on user query
6. Sends context and query to the language model
7. Returns a concise and relevant answer

---

Important Notes

- Do not upload "faiss_index/" to GitHub
- Ensure Ollama is running locally
- Run "vector_store.py" before starting the backend

---

Future Improvements

- Add chat history memory
- Improve UI design
- Support multiple documents
- Deploy using cloud platforms

