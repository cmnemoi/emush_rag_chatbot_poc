import logging
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from emush_rag_chatbot.llm import OpenAILLM
from emush_rag_chatbot.rag_chain import RAGChain
from emush_rag_chatbot.vector_store import ChromaVectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="eMush RAG Chatbot")

# Initialize RAG chain lazily
_rag_chain = None


def get_rag_chain() -> RAGChain:
    """Get or create RAG chain instance"""
    global _rag_chain
    if _rag_chain is None:
        _rag_chain = RAGChain(
            vector_store=ChromaVectorStore(),
            llm=OpenAILLM(),
        )
    return _rag_chain


class ChatRequest(BaseModel):
    """Schema for chat requests"""

    query: str
    chat_history: Optional[List[Dict[str, str]]] = None


class SourceDocument(BaseModel):
    """Schema for source documents used in responses"""

    content: str
    title: str
    source: str
    link: str


class ChatResponse(BaseModel):
    """Schema for chat responses"""

    response: str
    sources: List[SourceDocument]


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint that processes queries using RAG

    Args:
        request: ChatRequest containing query and optional parameters

    Returns:
        Generated response with source citations
    """
    try:
        rag_chain = get_rag_chain()
        response, sources = await rag_chain.generate_response(query=request.query, chat_history=request.chat_history)

        source_documents = [
            SourceDocument(
                content=doc.page_content,
                title=doc.metadata.get("title", ""),
                source=doc.metadata.get("source", ""),
                link=doc.metadata.get("link", ""),
            )
            for doc in sources
        ]

        return ChatResponse(response=response, sources=source_documents)

    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")
