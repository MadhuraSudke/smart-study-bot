# 📚 Smart Study Bot

An AI-powered study assistant built using Streamlit, LangChain, ChromaDB, HuggingFace Embeddings, Gemini, and Ollama.

The application allows students to ask questions from their study material, generate quizzes, create flashcards, and produce study summaries using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

### 🔍 Ask Questions

* Ask questions from uploaded study materials.
* Uses semantic search with ChromaDB.
* Supports conversational memory.
* Query rewriting for better retrieval accuracy.

### 📝 Quiz Generator

* Generates multiple-choice questions from study content.
* Includes correct answers and explanations.

### 🃏 Flashcard Generator

* Creates study flashcards automatically.
* Useful for revision and self-testing.

### 📖 Summary Generator

* Generates concise study guides.
* Extracts key concepts, definitions, and important points.

### 🧠 Retrieval-Augmented Generation (RAG)

* Retrieves relevant information from documents.
* Reduces hallucinations by grounding responses in source material.

---

## 🏗️ Tech Stack

### Frontend

* Streamlit

### Backend

* Python
* LangChain

### Vector Database

* ChromaDB

### Embeddings

* HuggingFace Embeddings
* Model: `sentence-transformers/all-MiniLM-L6-v2`

### Large Language Models

* Google Gemini 2.5 Flash
* Ollama (Llama 3.2)

---

## 📂 Project Structure

```text
smart-study-bot/

├── app.py
├── chat.py
├── ingest.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
├── chroma_db/
└── screenshots/
```

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/MadhuraSudke/smart-study-bot.git

cd smart-study-bot
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
```

---

## 📚 Build Vector Database

Run:

```bash
python ingest.py
```

This:

* Loads documents
* Creates embeddings
* Stores vectors in ChromaDB

---

## ▶️ Run Application

```bash
streamlit run app.py
```

---

## 🔄 Workflow

1. User asks a question.
2. Query is rewritten for better retrieval.
3. ChromaDB retrieves relevant chunks.
4. Retrieved context is sent to Gemini/Ollama.
5. Response is generated and displayed.

---

## 🎯 Future Improvements

* PDF upload support
* Source citations
* User authentication
* Cloud deployment
* Personalized study plans
* Progress tracking dashboard

---

## 👨‍💻 Author

Madhura Sudke

B.Tech Student | Artificial Intelligence & Data Science

---

## 📜 License

This project is developed for educational and learning purposes.
