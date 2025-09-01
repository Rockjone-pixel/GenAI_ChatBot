# 🤖 GenAIChatBot ~ RizzBot

A **document-aware, hallucination-resistant chatbot** built with **Gemini + LangChain + RAG + Embeddings**.  
This chatbot answers your queries from uploaded PDF notes, and if the answer isn’t present in your notes, it **falls back to Wikipedia** with a disclaimer.  

---

## Features :-
-  Upload **PDF notes** and ask questions directly.  
-  Uses **Retrieval-Augmented Generation (RAG)** to fetch answers from your notes.  
-  Falls back to **Wikipedia search** if the answer is not in the provided documents.  
-  Beautiful **Streamlit UI** with custom chat bubbles and Lottie animations.  
-  Reduces **hallucination problem** of LLMs by making sources transparent.  

---

## 🛠️ Tech Stack
- **Language Model:** Gemini 1.5 Flash (Google Generative AI)  
- **Frameworks & Libraries:**  
  - [LangChain](https://www.langchain.com/) – Document retrieval & chains  
  - [FAISS](https://github.com/facebookresearch/faiss) – Vector similarity search  
  - [PyPDF2](https://pypi.org/project/PyPDF2/) – Extract text from PDFs  
  - [Streamlit](https://streamlit.io/) – Interactive UI  
  - [Wikipedia API Wrapper](https://python.langchain.com/docs/integrations/tools/wikipedia) – External fallback  
  - [dotenv](https://pypi.org/project/python-dotenv/) – API key management  

---

## 🚀 How It Works
1. Upload your **PDF notes**.  
2. Notes are split into **chunks** and converted into **embeddings** using `GoogleGenerativeAIEmbeddings`.  
3. User queries are matched with the most relevant chunks using **FAISS similarity search**.  
4. If relevant context is found → Answer is generated using **Gemini LLM**.  
5. If no context → Fetch answer from **Wikipedia** and add a **clear disclaimer**.  

---

## 📂 Project Structure
