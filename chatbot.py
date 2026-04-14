from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

db = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

def clean(text):
    return text.lower().replace("?", "").strip()

def get_response(query):
    try:
        query_clean = clean(query)

        docs_with_score = db.similarity_search_with_score(query, k=5)

        best_answer = None
        best_score = 999

        for doc, score in docs_with_score:

            if score > 2.0:
                continue

            text = doc.page_content

            if "Q:" in text and "A:" in text:
                q_part = text.split("A:")[0].replace("Q:", "").strip()
                a_part = text.split("A:")[1].strip()

                q_clean = clean(q_part)

                # 🔥 STRICT MATCH (main fix)
                if query_clean == q_clean:

                    if score < best_score:
                        best_score = score
                        best_answer = a_part.split("\n")[0].strip()

        if not best_answer:
            return {
                "answer": "I don't know based on the provided information.",
                "sources": []
            }

        return {
            "answer": best_answer,
            "sources": ["pdf", "faq"]
        }

    except Exception as e:
        print(e)
        return {
            "answer": "Something went wrong.",
            "sources": []
        }