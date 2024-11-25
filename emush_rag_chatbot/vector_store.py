import logging
from typing import Any, Dict, List, Protocol, runtime_checkable

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from emush_rag_chatbot.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@runtime_checkable
class VectorStore(Protocol):
    """Abstract base class for vector stores"""

    async def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store"""
        ...

    def similarity_search(self, query: str, k: int, filter_metadata: Dict[str, Any] | None = None) -> List[Document]:
        """Perform similarity search with optional metadata filtering"""
        ...


class ChromaVectorStore(VectorStore):
    """Manages document embeddings and similarity search using Chroma"""

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL, openai_api_key=settings.OPENAI_API_KEY)
        self.vector_store = self._initialize_store()

    def _initialize_store(self) -> Chroma:
        """Initialize the vector store with persistence"""
        return Chroma(persist_directory=str(settings.CHROMA_PERSIST_DIR), embedding_function=self.embeddings)

    async def add_documents(self, documents: List[Document]) -> None:
        """
        Index documents in the vector store

        Args:
            documents: List of documents to index
        """
        try:
            await self.vector_store.aadd_documents(documents)
            logger.info(f"Successfully indexed {len(documents)} documents")
        except Exception as e:
            logger.error(f"Error indexing documents: {e}")
            raise

    def similarity_search(self, query: str, k: int, filter_metadata: Dict[str, Any] | None = None) -> List[Document]:
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


class FakeVectorStore(VectorStore):
    """A fake vector store implementation for testing"""

    def __init__(self, documents: List[Document] | None = None):
        self.documents = documents or []

    async def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the fake store"""
        self.documents.extend(documents)
        logger.info(f"Added {len(documents)} documents to fake store")

    def similarity_search(self, query: str, k: int, filter_metadata: Dict[str, Any] | None = None) -> List[Document]:
        """Return a subset of stored documents, ignoring actual similarity"""
        filtered_docs = self.documents
        if filter_metadata:
            filtered_docs = [
                doc
                for doc in self.documents
                if all(doc.metadata.get(key) == value for key, value in filter_metadata.items())
            ]
        return filtered_docs[:k]
