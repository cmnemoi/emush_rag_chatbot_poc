import asyncio
import logging
from typing import List
from tqdm import tqdm
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

        # Convert to Langchain documents
        langchain_docs = []
        for doc in documents:
            langchain_docs.append(
                LangchainDocument(
                    page_content=doc.content, metadata={"title": doc.title, "source": doc.source, "link": doc.link}
                )
            )

        # Process documents in batches
        batch_size = 50
        total_batches = (len(langchain_docs) + batch_size - 1) // batch_size
        
        with tqdm(total=total_batches, desc="Indexing documents") as pbar:
            for i in range(0, len(langchain_docs), batch_size):
                batch = langchain_docs[i:i + batch_size]
                await vector_store.add_documents(batch)
                pbar.update(1)
        
        logger.info(f"Successfully indexed {len(documents)} documents in {total_batches} batches")

    except Exception as e:
        logger.error(f"Error indexing documents: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
