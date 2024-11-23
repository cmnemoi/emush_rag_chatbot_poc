import asyncio
import logging
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

        # Load documents in batches
        document_batches = loader.load_documents()
        total_docs = 0

        # Process each batch
        for batch_idx, documents in enumerate(document_batches, 1):
            logger.info(f"Processing batch {batch_idx}")
            total_docs += len(documents)

            # Convert to Langchain documents
            langchain_docs = []
            for doc in documents:
                langchain_docs.append(
                    LangchainDocument(
                        page_content=doc.content, metadata={"title": doc.title, "source": doc.source, "link": doc.link}
                    )
                )

            # Index current batch
            await vector_store.add_documents(langchain_docs)
            logger.info(f"Successfully indexed batch {batch_idx}")

        logger.info(f"Successfully indexed {total_docs} documents in total")

    except Exception as e:
        logger.error(f"Error indexing documents: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
