from typing import List, Dict, Any
import logging

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from emush_rag_chatbot.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStore:
    """Manages document embeddings and similarity search"""

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL, openai_api_key=settings.OPENAI_API_KEY)
        self.vector_store = self._initialize_store()

    def _initialize_store(self) -> Chroma:
        """Initialize the vector store with persistence"""
        return Chroma(persist_directory=str(settings.CHROMA_PERSIST_DIR), embedding_function=self.embeddings)

    def add_documents(self, documents: List[Document]) -> None:
        """
        Index documents in the vector store

        Args:
            documents: List of documents to index
        """
        try:
            self.vector_store.add_documents(documents)
            logger.info(f"Successfully indexed {len(documents)} documents")
        except Exception as e:
            logger.error(f"Error indexing documents: {e}")
            raise

    def similarity_search(
        self, query: str, k: int = 4, filter_metadata: Dict[str, Any] | None = None
    ) -> List[Document]:
        """
        Perform similarity search with optional metadata filtering

        Args:
            query: Search query
            k: Number of results to return
            filter_metadata: Optional metadata filters

        Returns:
            List of relevant documents
        """
        try:
            return self.vector_store.similarity_search(query, k=k, filter=filter_metadata)
        except Exception as e:
            logger.error(f"Error performing similarity search: {e}")
            raise
