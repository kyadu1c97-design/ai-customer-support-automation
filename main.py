from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import get_response
from fastapi.middleware.cors import CORSMiddleware
import os

# ✅ Import vector store creator
from vector_store import create_vector_store

# ✅ Auto-create vector store if not exists (IMPORTANT for deploy)
try:
    if not os.path.exists("faiss_index"):
        print("⚡ Creating vector store automatically...")
        create_vector_store()
except Exception as e:
    print(f"⚠️ Error creating vector store: {e}")

app = FastAPI()

# CORS (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "AI Customer Support API is running 🚀"}


@app.get("/health")
def health():
    return {"status": "OK"}


@app.post("/chat")
def chat(query: Query):
    try:
        answer = get_response(query.question)
        return answer
    except Exception as e:
        return {"error": str(e)}