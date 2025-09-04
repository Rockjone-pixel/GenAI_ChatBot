import nest_asyncio
nest_asyncio.apply()

import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from docx import Document
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from dotenv import load_dotenv
from streamlit_lottie import st_lottie
import requests
import os

# =========================
# Load API Key
# =========================
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in environment variables")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# =========================
# Wikipedia Wrapper
# =========================
wiki = WikipediaAPIWrapper()

# =========================
# Helper for Lottie Animations
# =========================
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# =========================
# Custom Styling (CSS) - Mobile Responsive
# =========================
st.markdown("""
    <style>
    /* 🌐 Base Styling */
    .stApp {
        background: linear-gradient(to right, #141e30, #243b55);
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
        padding: 10px;
    }

    h1, h2, h3 {
        text-align: center;
        font-weight: 600;
        color: #f0f0f0;
        text-shadow: 1px 1px 3px #000;
        margin-bottom: 15px;
    }

    /* 💬 Chat Bubbles */
    .chat-bubble {
        padding: 12px;
        margin: 8px 0;
        border-radius: 12px;
        max-width: 85%;
        word-wrap: break-word;
        font-size: 16px;
        line-height: 1.4;
    }

    .user-bubble {
        background-color: #4CAF50;
        color: white;
        margin-left: auto;
        text-align: right;
    }

    .bot-bubble {
        background-color: #2a2a2a;
        color: #f8f8f8;
        margin-right: auto;
        text-align: left;
    }

    /* 📱 Tablet Screens */
    @media (max-width: 768px) {
        h1, h2, h3 {
            font-size: 22px !important;
        }
        .chat-bubble {
            font-size: 14px;
            padding: 10px;
            max-width: 95%;
        }
        .stMarkdown {
            font-size: 14px !important;
        }
    }

    /* 📱 Mobile Screens */
    @media (max-width: 480px) {
        h1, h2, h3 {
            font-size: 18px !important;
        }
        .chat-bubble {
            max-width: 100%;
            font-size: 13px;
        }
        .stButton>button {
            width: 100% !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# Header with Animation
# =========================
st.markdown("## 🤖 RizzBot – Your AI Tutor", unsafe_allow_html=True)

# Detect screen size dynamically
col1, col2 = st.columns([1, 3], gap="small")
with col1:
    lottie_robot = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")
    if lottie_robot:
        st_lottie(lottie_robot, height=120, key="robot")
with col2:
    st.write("")  # spacing
    st.write("")  # spacing
    st.subheader("Always here to help you learn 📚")

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.title("📚 My Notes")
    file = st.file_uploader(
        "Upload your notes (PDF, DOCX, or TXT)",
        type=["pdf", "docx", "txt"]
    )
    st.markdown("---")
    st.markdown("✨ Pro tip: Upload clear text-based files for best results.")
    st.markdown("💡 Try asking: *What are the key concepts in chapter 2?*")

# =========================
# Extracting Document Text
# =========================
if file is not None:
    try:
        text = ""

        # Handle PDF
        if file.type == "application/pdf":
            my_pdf = PdfReader(file)
            for page in my_pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

        # Handle DOCX
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(file)
            for para in doc.paragraphs:
                text += para.text + "\n"

        # Handle TXT
        elif file.type == "text/plain":
            text = file.read().decode("utf-8")

        # Safety check
        if not text.strip():
            st.warning("⚠️ Could not extract any text. File may be empty or unsupported.")
            st.stop()

        # Break into chunks
        splitter = RecursiveCharacterTextSplitter(
            separators=["\n"], chunk_size=1000, chunk_overlap=100
        )
        chunks = splitter.split_text(text)

        # Embeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(chunks, embeddings)

        # User Input
        user_query = st.text_input("💬 Ask me anything about your notes:")

        if user_query:
            with st.spinner("🤔 Thinking..."):
                # Search in document notes
                matching_chunks = vector_store.similarity_search(user_query, k=3)

                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    temperature=0.1
                )

                customized_prompt = ChatPromptTemplate.from_template(
                    """You are my assistant tutor. Answer the question based on the following context. 
                    If you did not get the context simply say "No notes context":

                    Context:
                    {context}

                    Question: {input}

                    Answer: """
                )

                chain = create_stuff_documents_chain(llm, customized_prompt)
                output = chain.invoke({"input": user_query, "context": matching_chunks})

                # Ensure string
                if isinstance(output, dict):
                    output = str(output.get("output_text", output))
                else:
                    output = str(output)

                # If no notes context → Wikipedia fallback
                if "No notes context" in output:
                    wiki_result = wiki.run(user_query)
                    if wiki_result:
                        words = wiki_result.split()
                        short_wiki_result = " ".join(words[:120]) + "..."

                        # Add styled Wikipedia disclaimer
                        disclaimer_html = """
                        <div style="
                            background-color:#FFD700; 
                            color:#000; 
                            padding:8px 12px; 
                            border-radius:8px; 
                            font-weight:bold; 
                            margin-bottom:10px;
                            text-align:center;">
                            📖 I couldn’t find it in your notes, but here’s a short summary from Wikipedia:
                        </div>
                        """

                        output = f"{disclaimer_html}<div>{short_wiki_result}</div>"

                # Chat UI
                st.markdown(f'<div class="chat-bubble user-bubble">{user_query}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chat-bubble bot-bubble">{output}</div>', unsafe_allow_html=True)

                st.success("✅ Response generated!")

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
