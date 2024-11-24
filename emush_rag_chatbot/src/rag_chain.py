from typing import List, Dict, Any, Optional, Tuple
import logging

from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from emush_rag_chatbot.config import settings
from emush_rag_chatbot.src.vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REFORMULATE_TEMPLATE = """You are an expert at reformulating questions about the eMush game.
Your task is to reformulate the user's question to make it clearer and more specific.
Keep the reformulated question concise and focused on the key information needed.
Maintain the original intent but make it more suitable for information retrieval.

Original question: {question}

Reformulated question:"""

SYSTEM_TEMPLATE = """You are an expert assistant for the eMush game.
Use the following pieces of retrieved context to answer questions about the game.
If you don't know the answer, just say that you don't know.
Keep answers concise and accurate.

Context:
{context}

"""

HUMAN_TEMPLATE = """Question: {question}

Previous conversation:
{chat_history}
"""


class RAGChain:
    """Implements the RAG pipeline for question answering"""

    def __init__(self):
        self.vector_store = VectorStore()
        self.llm = ChatOpenAI(
            model=settings.CHAT_MODEL, temperature=0, seed=42, openai_api_key=settings.OPENAI_API_KEY
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_TEMPLATE),
                ("human", HUMAN_TEMPLATE),
            ]
        )
        self.reformulate_prompt = ChatPromptTemplate.from_template(REFORMULATE_TEMPLATE)

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

    async def reformulate_question(self, query: str) -> str:
        """Reformulate the user's question to be more suitable for RAG"""
        chain = self.reformulate_prompt | self.llm | StrOutputParser()
        reformulated = await chain.ainvoke({"question": query})
        logger.info(f"Reformulated question: {reformulated}")
        return reformulated

    async def generate_response(
        self,
        query: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        filter_metadata: Optional[Dict[str, Any]] = None,
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
            # Reformulate the question
            reformulated_query = await self.reformulate_question(query)
            
            # Retrieve relevant documents using reformulated query
            docs = self.vector_store.similarity_search(reformulated_query, filter_metadata=filter_metadata)

            # Format inputs
            formatted_history = self._format_chat_history(chat_history)
            formatted_docs = self._format_docs(docs)

            logger.info(f"Retrieved {len(docs)} relevant documents")

            # Create and execute chain
            chain = (
                {
                    "context": lambda x: formatted_docs,
                    "question": lambda x: x["question"],
                    "chat_history": lambda x: formatted_history,
                }
                | self.prompt
                | self.llm
                | StrOutputParser()
            )

            response = await chain.ainvoke({"question": query})
            logger.info(f"Generated response for query: {query}")
            return response, docs

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
