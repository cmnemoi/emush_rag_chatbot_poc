import logging
from typing import Dict, List, Optional, Tuple

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from emush_rag_chatbot.config import settings
from emush_rag_chatbot.src.llm import LLM
from emush_rag_chatbot.src.prompts import PROMPTS
from emush_rag_chatbot.src.vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SYSTEM_TEMPLATE = PROMPTS[settings.PROMPT_VERSION]

HUMAN_TEMPLATE = """Question: {question}

Previous conversation:
{chat_history}
"""


class RAGChain:
    """Implements the RAG pipeline for question answering"""

    def __init__(self, vector_store: VectorStore, llm: LLM):
        self.vector_store = vector_store
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_TEMPLATE),
                ("human", HUMAN_TEMPLATE),
            ]
        )

    def _format_chat_history(self, history: Optional[List[Dict[str, str]]] = None) -> str:
        """Format chat history for context"""
        if not history:
            return "No previous conversation."
        return "\n".join([f"Human: {exchange['human']}\nAssistant: {exchange['assistant']}" for exchange in history])

    def _format_docs(self, docs: List[Document]) -> str:
        """Format retrieved documents for context"""
        return "\n\n".join(
            [
                f"Source ({doc.metadata.get('source', 'Unknown')}, {doc.metadata.get('link', '#')}): {doc.page_content}"
                for doc in docs
            ]
        )

    async def generate_response(
        self,
        query: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> Tuple[str, List[Document]]:
        """
        Generate a response using the RAG pipeline

        Args:
            query: User question
            chat_history: Optional conversation history
            filter_metadata: Optional metadata filters

        Returns:
            Generated response with source citations
        """
        try:
            # Retrieve relevant documents
            twinpedia_docs = self.vector_store.similarity_search(
                query, k=settings.TOP_K, filter_metadata={"source": "Twinpedia"}
            )
            mushpedia_docs = self.vector_store.similarity_search(
                query, k=settings.TOP_K, filter_metadata={"source": "Mushpedia"}
            )
            aide_aux_bolets_docs = self.vector_store.similarity_search(
                query, k=settings.TOP_K, filter_metadata={"source": "Aide aux Bolets"}
            )
            mush_forums_docs = self.vector_store.similarity_search(
                query, k=settings.TOP_K, filter_metadata={"source": "Mush Forums"}
            )

            docs = twinpedia_docs + mushpedia_docs + aide_aux_bolets_docs + mush_forums_docs

            # Format inputs
            formatted_history = self._format_chat_history(chat_history)
            formatted_docs = self._format_docs(docs)

            logger.info(f"Retrieved {len(docs)} relevant documents")

            # Format prompt
            prompt = self.prompt.format_messages(
                context=formatted_docs, question=query, chat_history=formatted_history
            )

            # Generate response directly using LLM
            response = await self.llm.invoke(prompt)

            return response, docs
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
