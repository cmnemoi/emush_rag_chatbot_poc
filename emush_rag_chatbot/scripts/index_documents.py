import asyncio
import logging
from pathlib import Path
from langchain_core.documents import Document as LangchainDocument

from emush_rag_chatbot.document_loader import DocumentLoader
from emush_rag_chatbot.src.vector_store import VectorStore
from emush_rag_chatbot.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Index documents from the data directory into the vector store"""
    try:
        # Initialize document loader and vector store
        loader = DocumentLoader(str(settings.DATA_DIR))
        vector_store = VectorStore()

        # Load documents
        documents = loader.load_documents()
        logger.info(f"Loaded {len(documents)} documents")

        # Convert to Langchain documents
        langchain_docs = []
        for doc in documents:
            langchain_docs.append(
                LangchainDocument(
                    page_content=doc.content,
                    metadata={
                        "title": doc.title,
                        "source": doc.source,
                        "link": doc.link
                    }
                )
            )

        # Index documents
        vector_store.add_documents(langchain_docs)
        logger.info("Successfully indexed all documents")

    except Exception as e:
        logger.error(f"Error indexing documents: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
