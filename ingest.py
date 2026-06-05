from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from dotenv import load_dotenv

load_dotenv()

# folder containing txt files
NOTES_FOLDER = r"D:\smart-study-bot\data\python"

documents = []

for file in Path(NOTES_FOLDER).glob("*.txt"):
    text = file.read_text(encoding="utf-8")

    documents.append(
        {
            "text": text,
            "source": file.name
        }
    )

print(f"Loaded {len(documents)} files")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = []

for doc in documents:
    split_texts = splitter.split_text(doc["text"])

    for chunk in split_texts:
        chunks.append(
            {
                "text": chunk,
                "source": doc["source"]
            }
        )

print(f"Created {len(chunks)} chunks")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

texts = [c["text"] for c in chunks]

metadatas = [
    {"source": c["source"]}
    for c in chunks
]

vectordb = Chroma.from_texts(
    texts=texts,
    embedding=embedding_model,
    metadatas=metadatas,
    persist_directory="chroma_db"
)

print("Vector database created successfully!")