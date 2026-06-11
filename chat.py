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

 # query Rewrting 

def rewrite_query(query, conversation_history, llm):

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
def retrieve_context(query, k=5):
   
   results = db.similarity_search_with_score(
      query,
      k=k
   )


   context = "\n\n".join(
      doc.page_content
      for doc, score in results
   )
   sources=[]
  # meta data key
   for doc , score in results:
      source = doc.metadata.get(
      "source",
      "unknown source"
    )

      if source not in sources:
         sources.append(source) 
   return context, sources 
      

# ask user for question , MAIN CHAT LOOP 
def ask_question(query, model_name="ollama"):
      # retiieval context 
    if model_name == "gemini":
      llm = gemini_llm
    else:
      llm = ollama_llm                                    
    # Retrival
# previously similarity_search returned document as object
# now it will return (document, score)

# retrieve relevent chunks
    conversation_history = get_recent_history()

    rewritten_query = rewrite_query(
    query,
    conversation_history,
    ollama_llm
    )

    context, sources = retrieve_context(
       rewritten_query,
        k=3
    )

    if not context.strip():
       return {
          "answer":
        "I could not find that information in the provided documents.",
        "rewritten_query": rewritten_query,
        "sources": []
    
       }
    prompt = f"""
          You are a study assistant.

          STRICT RULES:

          1. Use ONLY the information in the provided context.
          2. Do NOT use your own knowledge.
          3. If the answer cannot be found in the context, reply exactly:

          I could not find that information in the provided documents.
          
        conversation History :
        {conversation_history}
         
        context :
        {context}
        
        question:
        {query}
        
        Answer :
          """


# tuple unpacking , lower the score the better the result 
     

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

     if "RESOURCE_EXHAUSTED" in str(e):

        return {
            "answer":
            "Gemini quota exceeded. Please switch to Ollama or wait for quota reset.",
            "rewritten_query": "",
            "sources": []
        }

     return {
        "answer": f"Error: {str(e)}",
        "rewritten_query": "",
        "sources": []
       }
    

# quiz generator
def generate_quiz (topic,model_name="gemini"):
 llm= gemini_llm if model_name =="gemini" else ollama_llm

 context,sources = retrieve_context(
   topic, 
   k=5
   )

 prompt = f"""
   you are a study assitant.

    use the context below to create
    10 multiple-choice questions.property
    for each question include :
 
    Question 
    A)
    B)
    C)
    D)

    Correct Answer 
    Explanation
    context:
    {context}
    """

 response = llm.invoke(prompt)
 return{
   "quiz": response.content,
   "sources": sources
   }

#Flashcard Generator 
def generate_flashcards(topic,model_name="gemini"):
 
   llm = gemini_llm if model_name == "gemini"else ollama_llm
      
   context,sources = retrieve_context(
       topic, 
       k=5
    )


   prompt = f"""
        create 20 study flashcards.

           format:
           Question:
            ...
           Answer:
            ...

        context:
         {context}
           """
    
   response = llm.invoke(prompt)

   return {
        "flashcards" : response.content,
         "sources": sources
          }

# summmary generator 
def generate_summary(topic, model_name="gemini"):
   llm = gemini_llm if model_name =="gemini"else ollama_llm
      

   context, sources = retrieve_context(
   topic ,
   k=5
    )

   prompt = f"""
   create study guide 

    create a study guide .
    Include :
    1. key conepts
    2. definitions
    3. Important points
    4. Exam tips

    context :
     {context}
    """

   response = llm.invoke(prompt)

   return{
   "summary": response.content,
   "sources": sources
    }

# temp 
result = ask_question(
    "What is machine learning?",
    model_name="gemini"
)

print(result)