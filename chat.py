from dotenv import load_dotenv
import os

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_google_genai import ChatGoogleGenerativeAI

# loading api key

load_dotenv()

embedding_model = HuggingFaceEmbeddings(
    model_name ="sentence-transformers/all-MiniLM-L6-v2"
)

# load chroma database
db= Chroma(
    persist_directory="chroma_db",
    embedding_function= embedding_model
)

# load gemini
llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash"
)

# ask user for question
while True:
    query = input("Ask a question: ")      # retiieval context 
                                        
    if query.lower() == "exit":
        break



# previously similarity_search returned document as object
# now it will return (document, score)

# retrieve relevent chunks
    results = db.similarity_search_with_score(query,k=3)

    print("\nSimilarity Scores: ")
# tuple unpacking , lower the score the better the result 
    for doc, score in results:
     print(score)

    print("\nRetrieved Chunks:\n")

    for i, (doc, score) in enumerate(results, start=1):
     print(f"\nChunk {i}")
     print("-" * 50)
     print(f"Score: {score}")
     print(doc.page_content[:300])

# it's for showing sources 
    print("\nSources Used:")

    for i, (doc, score) in enumerate(results, start=1):
     print(f"{i}. {doc.metadata.get('source','unknown source')}")

    # type is list[tuple[document,float]]

# build context 
    context ="\n\n".join(
     doc.page_content 
     for doc, score in results 
     )


    prompt = f"""
        You are a helpful study assistant.

        Answer the question using ONLY the provided context.

        If the answer is not present in the context,
        say "I could not find that information in the provided documents."

        Context:
        {context}

        Question:
        {query}

        Answer:
        """

# call gemini
    response = llm.invoke(prompt)

# print answer 
    print("\nAnswer:\n")
    print(response.content)