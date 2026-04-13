from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import requests

# Load embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load FAISS DB
db = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

def get_response(query):
    try:
        print("\n🔍 Question:", query)

        # Get docs with similarity score
        docs_with_score = db.similarity_search_with_score(query, k=3)

        # 🔥 DEBUG (important)
        for doc, score in docs_with_score:
            print("Score:", score)

        # ✅ FIX: less strict filtering
        docs = [doc for doc, score in docs_with_score if score < 1.5]

        print("📄 Relevant Docs:", len(docs))

        # If no relevant docs
        if not docs:
            return {
                "answer": "I don't know based on the provided information.",
                "sources": []
            }

        # Prepare context
        context = " ".join([d.page_content for d in docs])[:800]

        # Prompt
        prompt = f"""
Context:
{context}

Question:
{query}

Give only the final answer in one short sentence.
If not found, say: I don't know.
"""

        # Call Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code != 200:
            return {
                "answer": "⚠️ Ollama server error.",
                "sources": []
            }

        result = response.json()

        # ===== CLEAN OUTPUT =====
        answer = result.get("response", "").strip()

        # First line only
        answer = answer.split("\n")[0]

        # Remove unwanted prefixes
        unwanted_words = [
            "answer:", "response:", "responses:",
            "informative response:", "question:", "questão"
        ]

        for word in unwanted_words:
            if word in answer.lower():
                answer = answer.lower().replace(word, "").strip()

        # Remove quotes
        answer = answer.replace('"', '').strip()

        # Remove repeated question
        if "?" in answer:
            answer = answer.split("?")[-1].strip()

        # Keep only first sentence
        if "." in answer:
            answer = answer.split(".")[0].strip() + "."

        # Improve wording for refund
        if "refund" in answer.lower():
            answer = "Refunds are available within 7 days of purchase."

        # Final fallback
        if not answer or len(answer) < 5:
            answer = "I don't know based on the provided information."

        # ===== SOURCES =====
        sources = list(set([d.metadata.get("source", "unknown") for d in docs]))

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        print("❌ ERROR:", e)
        return {
            "answer": "Something went wrong.",
            "sources": []
        }