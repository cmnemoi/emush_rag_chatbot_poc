import pytest
from langchain_core.documents import Document

from emush_rag_chatbot.llm import FakeLLM
from emush_rag_chatbot.rag_chain import RAGChain
from emush_rag_chatbot.vector_store import FakeVectorStore


@pytest.fixture
def test_documents():
    return [
        Document(
            page_content="Mushrooms are fungi", metadata={"source": "Twinpedia", "link": "http://test.com/mushrooms"}
        ),
        Document(
            page_content="Bolets are a type of mushroom",
            metadata={"source": "Aide aux Bolets", "link": "http://test.com/bolets"},
        ),
    ]


@pytest.fixture
def fake_vector_store(test_documents):
    return FakeVectorStore(documents=test_documents)


@pytest.fixture
def fake_llm():
    return FakeLLM(response="This is a test response about mushrooms")


@pytest.fixture
def rag_chain(fake_vector_store, fake_llm):
    return RAGChain(vector_store=fake_vector_store, llm=fake_llm)


@pytest.mark.asyncio
async def test_generate_response_basic(rag_chain):
    """Test basic response generation without chat history"""
    response, docs = await rag_chain.generate_response("What are mushrooms?")

    assert isinstance(response, str)
    assert len(response) > 0
    assert isinstance(docs, list)
    assert all(isinstance(doc, Document) for doc in docs)


@pytest.mark.asyncio
async def test_generate_response_with_chat_history(rag_chain):
    """Test response generation with chat history"""
    chat_history = [{"human": "What are mushrooms?", "assistant": "Mushrooms are fungi"}]

    response, docs = await rag_chain.generate_response("Tell me more about bolets", chat_history=chat_history)

    assert isinstance(response, str)
    assert len(response) > 0
    assert isinstance(docs, list)
    assert all(isinstance(doc, Document) for doc in docs)


def test_format_chat_history(rag_chain):
    """Test chat history formatting"""
    chat_history = [{"human": "What are mushrooms?", "assistant": "Mushrooms are fungi"}]

    formatted = rag_chain._format_chat_history(chat_history)
    assert "Human: What are mushrooms?" in formatted
    assert "Assistant: Mushrooms are fungi" in formatted


def test_format_docs(rag_chain, test_documents):
    """Test document formatting"""
    formatted = rag_chain._format_docs(test_documents)

    assert "Source (Twinpedia" in formatted
    assert "Mushrooms are fungi" in formatted
    assert "Source (Aide aux Bolets" in formatted
    assert "Bolets are a type of mushroom" in formatted


def test_empty_chat_history(rag_chain):
    """Test formatting empty chat history"""
    assert rag_chain._format_chat_history(None) == "No previous conversation."
    assert rag_chain._format_chat_history([]) == "No previous conversation."
