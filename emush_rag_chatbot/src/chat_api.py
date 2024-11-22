from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

from emush_rag_chatbot.src.rag_chain import RAGChain

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="eMush RAG Chatbot")
rag_chain = RAGChain()


class ChatRequest(BaseModel):
    """Schema for chat requests"""

    query: str
    chat_history: Optional[List[Dict[str, str]]] = None
    filter_metadata: Optional[Dict[str, Any]] = None


class SourceDocument(BaseModel):
    """Schema for source documents used in response"""

    content: str
    metadata: Dict[str, Any]


class ChatResponse(BaseModel):
    """Schema for chat responses"""

    response: str
    source_documents: List[SourceDocument]


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
        response = await rag_chain.generate_response(
            query=request.query, chat_history=request.chat_history, filter_metadata=request.filter_metadata
        )
        return ChatResponse(
            response=response["response"],
            source_documents=[SourceDocument(**doc) for doc in response["source_documents"]],
        )

    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")
