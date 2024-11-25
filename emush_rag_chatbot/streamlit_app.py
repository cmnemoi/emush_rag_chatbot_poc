import asyncio
import json
from pathlib import Path
from typing import Dict, List

import httpx
import streamlit as st
from pydantic import BaseModel

# Configure page and paths
STATIC_DIR = Path(__file__).parent / "static"
st.set_page_config(
    page_title="eMush RAG Chatbot",
    page_icon="🍄",
    layout="wide",
)


class ChatMessage(BaseModel):
    """Chat message model for history"""

    human: str
    assistant: str


def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def display_chat_history():
    """Display chat history"""
    for message in st.session_state.messages:
        with st.chat_message("user", avatar=str(STATIC_DIR / "lambda_f.png")):
            st.markdown(message["human"])
        with st.chat_message("assistant", avatar=str(STATIC_DIR / "neron_eye.gif")):
            st.markdown(message["assistant"])
            if "sources" in message:
                with st.expander("View sources"):
                    for source in message["sources"]:
                        st.markdown(f"**{source['source']}** ([link]({source['link']}))\n\n{source['content']}\n\n---")


async def query_chatbot(question: str, chat_history: List[Dict[str, str]]) -> Dict:
    """Query the chatbot API"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8000/chat",
                json={"query": question, "chat_history": chat_history},
                timeout=30.0,
            )
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except httpx.HTTPError as e:
            st.error(f"HTTP Error: {str(e)}")
            return {"error": str(e)}
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return {"error": str(e)}


def main():
    """Main Streamlit app"""
    st.title("🍄 eMush RAG Chatbot")
    st.markdown(
        """
        Ask questions about the eMush game! The chatbot uses Retrieval-Augmented Generation (RAG) 
        to provide accurate answers based on wikis, tutorials and QA Mush forums.
        """
    )

    initialize_session_state()
    display_chat_history()

    # Chat input
    if question := st.chat_input("Ask a question about eMush"):
        with st.chat_message("user", avatar=str(STATIC_DIR / "lambda_f.png")):
            st.markdown(question)

        with st.chat_message("assistant", avatar=str(STATIC_DIR / "neron_eye.gif")):
            with st.spinner("Thinking..."):
                try:
                    response = asyncio.run(query_chatbot(question, st.session_state.chat_history))

                    if "error" in response:
                        st.error(response["error"])
                        return

                    # Display response
                    st.markdown(response["response"])

                    # Show sources
                    if response["sources"]:
                        with st.expander("View sources"):
                            for source in response["sources"]:
                                st.markdown(
                                    f"**{source['source']}** ([link]({source['link']}))\n\n{source['content']}\n\n---"
                                )

                    # Update chat history
                    st.session_state.messages.append(
                        {
                            "human": question,
                            "assistant": response["response"],
                            "sources": response["sources"],
                        }
                    )
                    st.session_state.chat_history.append({"human": question, "assistant": response["response"]})

                except Exception as e:
                    st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
