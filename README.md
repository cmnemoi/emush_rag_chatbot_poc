# eMush RAG Chatbot

[![Continuous Integration](https://github.com/cmnemoi/emush_rag_chatbot_poc/actions/workflows/continuous_integration.yaml/badge.svg)](https://github.com/cmnemoi/emush_rag_chatbot_poc/actions/workflows/continuous_integration.yaml)
[![Continuous Delivery](https://github.com/cmnemoi/emush_rag_chatbot_poc/actions/workflows/create_github_release.yaml/badge.svg)](https://github.com/cmnemoi/emush_rag_chatbot_poc/actions/workflows/create_github_release.yaml)
[![codecov](https://codecov.io/gh/cmnemoi/emush_rag_chatbot_poc/graph/badge.svg?token=FLAARH38AG)](https://codecov.io/gh/cmnemoi/emush_rag_chatbot_poc)

A Retrieval-Augmented Generation (RAG) chatbot that can answer questions about the eMush game using official documentation and community resources.

## Features

- Semantic search across eMush documentation
- Context-aware responses using GPT-4
- FastAPI-powered REST API
- Source attribution for transparency

## Installation

You need to have `curl` and [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed on your system.

Then run the following command:
```bash
curl -sSL https://raw.githubusercontent.com/cmnemoi/emush_rag_chatbot_poc/main/clone-and-install | bash
```

## Configuration

Create a `.env` file in the project root with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

Start the API server:
```bash
uv run emush_rag_chatbot/main.py
```

The API will be available at `http://localhost:8000` with Swagger documentation at `/docs`.

### Example API Request

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
           "query": "What are the basic actions in eMush?",
         }'
```

## Development

Run tests with:
```bash
make test
```

## License

The source code of this repository is licensed under the [AGPL-3.0-or-later License](LICENSE).
