# 🤖 GenAIChatBot ~ RizzBot

A document-aware, hallucination-resistant chatbot built with Gemini + LangChain + RAG + Embeddings.
This chatbot answers your queries from uploaded PDF, DOCX, and TXT notes, and if the answer isn’t present in your notes, it falls back to Wikipedia with a disclaimer.

Features :-

Upload PDF, DOCX, or TXT notes and ask questions directly.

Uses Retrieval-Augmented Generation (RAG) to fetch answers from your notes.

Falls back to Wikipedia search if the answer is not in the provided documents.

Beautiful Streamlit UI with custom chat bubbles and Lottie animations.

Reduces hallucination problem of LLMs by making sources transparent.

🛠️ Tech Stack

Language Model: Gemini 1.5 Flash (Google Generative AI)

Frameworks & Libraries:

LangChain
 – Document retrieval & chains

FAISS
 – Vector similarity search

PyPDF2
 – Extract text from PDFs

python-docx
 – Extract text from DOCX

Built-in Python file handling for .txt files

Streamlit
 – Interactive UI

Wikipedia API Wrapper
 – External fallback

dotenv
 – API key management

🚀 How It Works

Upload your PDF, DOCX, or TXT notes.

Notes are split into chunks and converted into embeddings using GoogleGenerativeAIEmbeddings.

User queries are matched with the most relevant chunks using FAISS similarity search.

If relevant context is found → Answer is generated using Gemini LLM.

If no context → Fetch answer from Wikipedia and add a clear disclaimer.

---

## 📂 Project Structure
