from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

load_dotenv()

app = FastAPI()

CHROMA_DIR = "chroma_db"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

@app.get("/")
def home():
    return {"message": "Security Incident Assistant running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    content = await file.read()
    text = content.decode("utf-8")

    chunks = text_splitter.split_text(text)

    docs = [Document(page_content=chunk) for chunk in chunks]

    vectorstore = Chroma.from_documents(
        docs,
        embedding_model,
        persist_directory=CHROMA_DIR
    )

    vectorstore.persist()

    return {
        "message": "File uploaded and indexed successfully",
        "chunks": len(chunks)
    }

@app.get("/ask")
def ask_question(query: str):

    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding_model
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    relevant_docs = retriever.invoke(query)

    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    prompt = f"""
You are a cybersecurity assistant reviewing log evidence.

Analyze the following security incident context:

{context}

Question:
{query}

Provide:
1. Incident summary
2. Severity
3. Possible threat explanation
4. Recommended remediation actions
"""

    response = llm.invoke(prompt)

    return {
        "question": query,
        "answer": response.content
    }