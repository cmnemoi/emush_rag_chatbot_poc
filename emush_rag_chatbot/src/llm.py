import logging
from typing import Any, Dict, Protocol, runtime_checkable

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

from emush_rag_chatbot.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@runtime_checkable
class LLM(Protocol):
    """Base interface for language models"""

    async def invoke(self, input: Dict[str, Any] | list[BaseMessage], config: Dict[str, Any] | None = None) -> str:
        """Invoke the language model with the given input"""
        ...


class OpenAILLM(LLM):
    """OpenAI language model implementation"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.CHAT_MODEL,
            temperature=settings.TEMPERATURE,
            seed=settings.SEED,
            openai_api_key=settings.OPENAI_API_KEY,
        )

    async def invoke(self, input: Dict[str, Any] | list[BaseMessage], config: Dict[str, Any] | None = None) -> str:
        """Invoke the OpenAI language model"""
        try:
            result = await self.llm.ainvoke(input)
            return result.content
        except Exception as e:
            logger.error(f"Error invoking OpenAI LLM: {e}")
            raise


class FakeLLM(LLM):
    """Fake language model for testing"""

    def __init__(self, response: str = "This is a test response"):
        self.response = response

    async def invoke(self, input: Dict[str, Any] | list[BaseMessage], config: Dict[str, Any] | None = None) -> str:
        """Return a predefined response for testing"""
        logger.info(f"FakeLLM received input: {input}")
        return self.response
