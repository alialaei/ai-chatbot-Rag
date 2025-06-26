from __future__ import annotations

import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from pydantic import BaseModel, Field, ValidationError
from qdrant_client import QdrantClient

# ---------------------------------------------------------------------------
# Environment & Qdrant initialisation
# ---------------------------------------------------------------------------

auth_env = load_dotenv()

QDRANT_URL: str | None = os.getenv("QDRANT_URL", "http://localhost:6333")

if not QDRANT_URL:
    raise RuntimeError(
        "QDRANT_URL environment variable must be set (e.g. http://localhost:6333)"
    )

qdrant_client = QdrantClient(url=QDRANT_URL)

def _collection_name(client_id: str) -> str:
    """Return deterministic collection name for a given client."""
    return f"client_{client_id}"

# ---------------------------------------------------------------------------
# Ingestion helpers
# ---------------------------------------------------------------------------

class IngestionStatus(BaseModel):
    """Return object after storing document chunks."""

    client_id: str = Field(..., description="Tenant identifier")
    chunks_stored: int = Field(..., ge=1)
    collection_name: str


def load_and_store_pdf(file_path: str | Path, client_id: str) -> IngestionStatus:
    """Parse *file_path* PDF, split, embed and store under the client's collection.

    Parameters
    ----------
    file_path : str | Path
        Path to the PDF on local filesystem.
    client_id : str
        Unique tenant identifier (e.g. UUID or slug).
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(file_path)

    loader = PyPDFLoader(str(file_path))
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    collection_name = _collection_name(client_id)

    Qdrant.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        client=qdrant_client,
    )

    return IngestionStatus(
        client_id=client_id, chunks_stored=len(chunks), collection_name=collection_name
    )

# ---------------------------------------------------------------------------
# Retrieval helpers
# ---------------------------------------------------------------------------

def search_and_answer(question: str, client_id: str, *, k: int = 3) -> str:
    """Answer *question* using documents previously ingested for *client_id*.

    Parameters
    ----------
    question : str
        Natural language query.
    client_id : str
        Tenant identifier used to scope vector search.
    k : int, optional
        Number of nearest chunks to retrieve, by default 3.
    """
    collection_name = _collection_name(client_id)

    vector_store = Qdrant(
        client=qdrant_client,
        collection_name=collection_name,
        embeddings=OpenAIEmbeddings(),
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": k})

    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-4"),
        retriever=retriever,
        chain_type="stuff",
    )

    return qa_chain.run(question)