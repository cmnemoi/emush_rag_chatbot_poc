# eMush RAG Chatbot

[![Continuous Integration](https://github.com/cmnemoi/emush_rag_chatbot_poc/actions/workflows/continuous_integration.yaml/badge.svg)](https://github.com/cmnemoi/emush_rag_chatbot_poc/actions/workflows/continuous_integration.yaml)
[![Continuous Delivery](https://github.com/cmnemoi/emush_rag_chatbot_poc/actions/workflows/create_github_release.yaml/badge.svg)](https://github.com/cmnemoi/emush_rag_chatbot_poc/actions/workflows/create_github_release.yaml)
[![codecov](https://codecov.io/gh/cmnemoi/emush_rag_chatbot_poc/graph/badge.svg?token=FLAARH38AG)](https://codecov.io/gh/cmnemoi/emush_rag_chatbot_poc)

A Retrieval-Augmented Generation (RAG) chatbot that can answer questions about the eMush game using wikis, tutorials and QA Mush forums.

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

## Usage

A tiny indexed Chroma vector database (emush_rag_chatbot/chroma_db/chroma.sqlite2) with some data ([emush_rag_chatbot/data/data.json](emush_rag_chatbot/data/data.json)) is included in the repository to get started.

Start the API server:
```bash
make run-chatbot
```

The API will be available at `http://localhost:8000` with Swagger documentation at `/docs`.

### Example API Request

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
           "query": "What is the goal of the game?",
         }'
```

## Development

### Better RAG performance

To get more accurate answers, you need more indexed data.

For this, use [Mush Wikis Scraper](https://github.com/cmnemoi/mush_wikis_scraper) to download all knowledge base of the commmunity : `uvx --from mush-wikis-scraper mush-wiki-scrap --format text > emush_rag_chatbot/data/data.json`

Then index the data in vector storewith: `make index-documents`

### Testing

Run tests with:
```bash
make test
```

## License

The source code of this repository is licensed under the [AGPL-3.0-or-later License](LICENSE).
