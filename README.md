# AI Security Incident Assistant

A small **FastAPI** service that implements **RAG (Retrieval-Augmented Generation)** over uploaded security logs: text is chunked, embedded with a **sentence-transformers** model, stored in **Chroma**, and questions are answered with **Groq** (Llama 3.1) using the most relevant log snippets as context.

## Features

- **`POST /upload`** — upload a UTF-8 text/log file; chunks are embedded and indexed locally.
- **`GET /ask?query=...`** — retrieve top similar chunks, build a prompt, return an LLM analysis (summary, severity, threat, remediation).
- **`GET /`** — health check JSON.
- **`GET /docs`** — interactive OpenAPI (Swagger) UI.

## Prerequisites

- **Python 3.12+** 
- A **Groq API key** ([Groq Console](https://console.groq.com/)).

## Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy the example environment file and add your key:

```powershell
copy .env.example .env
# Edit .env and set GROQ_API_KEY
```


## Run the API

```powershell
.\venv\Scripts\Activate.ps1
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Wait until the log shows **`Application startup complete.`** On the first run, the embedding model may download from Hugging Face (can take several minutes).

Then open:

- **http://127.0.0.1:8000/** — health JSON  
- **http://127.0.0.1:8000/docs** — try **upload** then **ask**

## Typical flow

1. **`POST /upload`** — choose a file such as `sample.log`.
2. **`GET /ask`** — e.g. query `What suspicious activity do you see?`

Indexed data is stored under **`chroma_db/`** (local, recreated by uploads;)

## Stack (high level)

| Piece        | Role |
|-------------|------|
| **FastAPI** | HTTP API and automatic OpenAPI docs. |
| **Uvicorn** | ASGI server. |
| **LangChain** | Chains splitting, Chroma, embeddings, Groq chat. |
| **Chroma**  | Local vector store (`chroma_db`). |
| **sentence-transformers / HF** | Embeddings model `all-MiniLM-L6-v2`. |
| **Groq**    | Hosted LLM (`llama-3.1-8b-instant`). |


## License

No license is set by default; 
