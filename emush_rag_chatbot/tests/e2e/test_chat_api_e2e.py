import os

import pytest
from fastapi.testclient import TestClient

from emush_rag_chatbot.chat_api import ChatRequest, ChatResponse, app


@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Set up test environment variables"""
    # Skip tests if OPENAI_API_KEY is not set
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY environment variable not set")


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_chat_endpoint_basic(client):
    """Test basic chat interaction without history"""
    request = ChatRequest(query="What are mushrooms in eMush?")
    response = client.post("/chat", json=request.model_dump())
    assert response.status_code == 200

    # Validate response format
    chat_response = ChatResponse(**response.json())
    assert isinstance(chat_response.response, str)
    assert len(chat_response.response) > 0
    assert isinstance(chat_response.sources, list)

    # Validate source documents
    for source in chat_response.sources:
        assert source.content
        assert source.source in ["Twinpedia", "Mushpedia", "Aide aux Bolets", "Mush Forums"]
        assert source.link
