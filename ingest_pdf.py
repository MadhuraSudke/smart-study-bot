from langchain_community.document_loaders import PyPDFLoader

print("INGEST_PDF STARTED")

from langchain_community.document_loaders import PyPDFLoader

print("IMPORT SUCCESSFUL")

pdf_path = input("Enter PDF name: ")

loader = PyPDFLoader(pdf_path)

documents = loader.load()

print("Loaded", len(documents), "pages")


print("PDF Loaded Successfully")
print(type(documents))
print(len(documents))
print(documents[0].metadata)
print(documents[0].page_content[:300])