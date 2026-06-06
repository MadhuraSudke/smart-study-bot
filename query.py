from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

query = "What are Python variables?"

results = db.similarity_search(query, k=3)

print("\nTop Results:\n")

for i, doc in enumerate(results, start=1):
    print(f"\nResult {i}:")
    print(doc.page_content)
    print("-" * 50)