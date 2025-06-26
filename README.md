# 🧠 AI Chatbot with RAG (LangChain + OpenAI + Qdrant)

This project is a customizable AI chatbot powered by **FastAPI**, **LangChain**, **OpenAI (GPT-4)**, and **Qdrant**. It uses **Retrieval-Augmented Generation (RAG)** to answer user queries based on uploaded PDFs — designed for business-specific, multi-tenant, or domain-aware chatbot use cases.

---

## 📦 Features

- ✨ GPT-4 integration via OpenAI API
- 📄 Upload and embed PDF documents (per `client_id`)
- 🔍 Fast semantic vector search using Qdrant
- 🧠 RAG-based contextual answer generation via LangChain
- 🚀 FastAPI backend with clean and minimal endpoints
- ✅ Type-annotated, commented, and production-ready code

---

## 🗂 Project Structure

ai-chatbot-rag/
├── main.py # FastAPI app with /chat and /upload-docs endpoints
├── rag_engine.py # Core RAG logic (load/store/retrieve/answer)
├── requirements.txt # Python dependencies (pinned to minor versions)
├── .env.example # Sample environment config
├── temp/ # Temporary PDF upload folder (git-ignored)
└── README.md # This file

yaml
Copy
Edit

---

## 🚀 Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/alialaei/ai-chatbot-rag.git
cd ai-chatbot-rag
2. Setup environment
bash
Copy
Edit
cp .env.example .env
# Edit .env and add your OpenAI API key and Qdrant URL
3. Create and activate a virtual environment
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
4. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
5. Start Qdrant (via Docker)
bash
Copy
Edit
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
6. Run the FastAPI server
bash
Copy
Edit
uvicorn main:app --reload
Visit: http://localhost:8000/docs to try the API.

🧪 API Endpoints
POST /upload-docs
Upload a PDF file for a specific client ID.

Request

form
Copy
Edit
client_id: your_client_slug_or_uuid
file: sample.pdf
POST /chat
Ask a question related to uploaded documents.

Request

json
Copy
Edit
{
  "client_id": "your_client_slug_or_uuid",
  "message": "What are the terms of the contract?"
}
🧰 Environment Variables
Create a .env file like:

env
Copy
Edit
OPENAI_API_KEY=sk-...
QDRANT_URL=http://localhost:6333
📝 TODO / Future Enhancements
✅ Add support for multi-file upload

🔒 Add authentication (JWT or OAuth)

🌐 Add frontend interface (React)

📈 Dashboard for usage metrics

🧪 Unit & integration tests

📄 License
MIT — feel free to use, fork, and contribute.

👨‍💻 Author
Created by Ali Alaei – CTO, backend/devops engineer & open-source enthusiast.