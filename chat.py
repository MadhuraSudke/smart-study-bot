from dotenv import load_dotenv
import os
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_google_genai import ChatGoogleGenerativeAI

# loading api key load environemnt variable

load_dotenv()

# load embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name ="sentence-transformers/all-MiniLM-L6-v2"
)

# load chroma database
db= Chroma(
    persist_directory="chroma_db",
    embedding_function= embedding_model
)

# load gemini
gemini_llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash"
)

ollama_llm = ChatOllama(
    model="llama3.2"
)

CURRENT_MODEL = "ollama"


if CURRENT_MODEL == "gemini":
    llm = gemini_llm
else:
    llm = ollama_llm

# conversation memory 
history =[]

MAX_HISTORY =10

def get_recent_history():
   """
   Return the most recent conversation messages.
   """
   recent_messages = history[-MAX_HISTORY:]

   conversation_text =" "
   for msg in recent_messages:
      conversation_text += (
         f"{msg['role'].capitalize()}:"
         f"{msg['content']}\n"
        )
   return conversation_text


def rewrite_query(query, conversation_history):

    rewrite_prompt = f"""
    Conversation History:
    {conversation_history}

    Current Question:
    {query}

    Rewrite the current question so it is a complete standalone question.

    Return ONLY the rewritten question.
    """

    response = llm.invoke(rewrite_prompt)

    return response.content.strip()

# ask user for question , MAIN CHAT LOOP 
def ask_question(query):
      # retiieval context 
                                          
    # Retrival
# previously similarity_search returned document as object
# now it will return (document, score)

# retrieve relevent chunks
    conversation_history = get_recent_history()

    rewritten_query = rewrite_query(
    query,
    conversation_history
    )


    results = db.similarity_search_with_score(
    rewritten_query,
    k=3
    )

    sources = []

    for doc, score in results:
       sources.append(
        doc.metadata.get(
            "source",
            "unknown source"
              )
        )
       

# tuple unpacking , lower the score the better the result 
     
     

# it's for showing sources 

    # type is list[tuple[document,float]]

# build context 
    context ="\n\n".join(
     doc.page_content 
     for doc, score in results 
     )
   
# get memory
    conversation_history = get_recent_history()

    # build prompt

    prompt = f"""
        You are a helpful study assistant.

        use the conversation histroy when relevent.

        Answer the question using ONLY the provided context.

        If the answer is not present in the context,
        say "I could not find that information in the provided documents."

        conversation Histroy:
        {conversation_history}

        Context:
        {context}

        Question:
        {query}

        Answer:
        """


    # call gemini
    try:
        response = llm.invoke(prompt)

        # save memory
        history.append(
           {
            "role": "user",
           "content": query
           }
        )

        history.append(
           {
              "role": "assistant",
              "content": response.content 
           }
        )

        return {
              "answer": response.content,
              "rewritten_query": rewritten_query,
              "sources": sources
               }

        # debug memory 
         
           
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "rewritten_query": " ",
            "sources" : []
        }
for msg in history:
         print(msg)

result1 = ask_question(
    "What is a transformer?"
)

print(result1["answer"])

result2 = ask_question(
    "Who introduced it?"
)

print(result2["answer"])
