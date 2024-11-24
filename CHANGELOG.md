# CHANGELOG


## v0.1.0 (2024-11-24)

### Bug Fixes

- Make document indexing asynchronous with await for vector store
  ([`75ac781`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/75ac781efd7962c4cca91d773bb796756b1ed862))

### Documentation

- Update README with correct command to run the application
  ([`0c89bf9`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/0c89bf960c8cda7cf6fd0d90d0af6afe26a08886))

- Update README to use uv for running Python scripts
  ([`e4a1c3c`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/e4a1c3cb99a19844d4e90679e399d8d7cf9eeee6))

- Update README with detailed project description and usage instructions
  ([`874be74`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/874be7402eac882c745ae37bd70c3b40799d9259))

### Features

- Add initial dummy test in test_main.py for basic validation of test structure
  ([`1ba149a`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/1ba149aba4ce9898042542d2d1fb758383f3017d))

- Refactor chat API to remove unnecessary filter_metadata; update vector store and dependencies for
  better performance and stability
  ([`7bf039f`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/7bf039fc1dbb1be3da5f6bd1206595b39f2cd3bb))

- Update CHAT_MODEL to "gpt-4o-mini" and switch evaluation dataset to "test_set_v3.csv" for improved
  chatbot performance
  ([`6e536bc`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/6e536bce2e711a08bb52f58913121e11d0c33b9c))

- Update chat model to "gpt-4o" and amend evaluation results for consistency in eMush chatbot
  configuration and responses
  ([`20f3645`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/20f3645fa64e80dc860e3d491eb23c513735390c))

- Add prompt template for version V6 to enhance context handling and reasoning in eMush chatbot
  responses
  ([`50e36e8`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/50e36e8f6141990df55417fcefb97dcc9a99d354))

- Remove redundant import of app in main.py for cleaner entry point structure
  ([`659ecde`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/659ecde4af5af230462a06f8d1280c01d267e6c3))

- Update prompt templates in RAGChain for versions V4 and V5 with enhanced reasoning requirements
  ([`a0b68f1`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/a0b68f1e28ec5223680949389663285f81f5f1f0))

- Enhance RAGChain to utilize versioned prompt templates for improved context handling
  ([`9aa4b98`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/9aa4b98bd7a8cce12611e8e035450dae63e93b48))

- Allow configuring top_k for document retrieval in RAGChain
  ([`6d9d827`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/6d9d827ce9503c3e88d129fb40e3755b734ff0b2))

- Save evaluation results to JSON with metadata and nested structure
  ([`1a81f37`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/1a81f3764fcbfe94e29ce3d62eb2c9b7236f5a61))

- Add question reformulation step to RAG chain for improved context retrieval
  ([`990008d`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/990008de6c63305998c6244cd60dcc268d132f1b))

- Enhance evaluation results storage with UUID, timestamp, and CSV export
  ([`068135d`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/068135da4969c380caef837ce44d74313b62b806))

- Add new Makefile targets for RAG evaluation, document indexing, and chatbot execution scripts
  ([`e1a761d`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/e1a761dca3f1a2915693a0435b69a471397ac756))

- Enhance RAG evaluation script with improved response evaluation and add test data for
  comprehensive assessments
  ([`905beab`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/905beab1a4272e99492e6d1498d15ed47ddc859f))

- Update DocumentLoader to allow larger chunk sizes and improved document splitting logic for long
  texts
  ([`8239850`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/82398504c78f0bc686613451f0b8f5c52de54558))

- Add RAG evaluation script with LLM-as-a-judge functionality
  ([`f471855`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/f471855e0e90a708146a3474ae1fc070ecbb7558))

- Modify chat API to return source documents with response
  ([`ab52c94`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/ab52c94202d840082428fddc5732a2edf5c41d0c))

- Add batch processing and tqdm progress bar for document indexing
  ([`de3a224`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/de3a22452ebdf1f0a14c3deb9d04b3b9e4f94be1))

- Restore batch processing for document indexing
  ([`5cccc32`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/5cccc3219d9fe504d84dcc7de25008779d531596))

- Add RecursiveCharacterTextSplitter to handle long document chunks
  ([`01261d9`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/01261d9a4fcc000f916c9b61bb783bc1590c5339))

- Update document loader to show loading progress and change batch size from 10 to 8
  ([`d272ad1`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/d272ad11e0088e013f6e4db7d68f3c35ed85a151))

- Return response with source documents in RAG chain
  ([`de0351a`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/de0351ade4d1c957d1a17678dcb7c4a0c3e4fae9))

- Add document batching to avoid OpenAI API rate limits
  ([`56bf522`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/56bf5226e106ad5317c698d3cd60cd48f1bf72b4))

- Add title to document metadata in document loader
  ([`ad07daa`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/ad07daaaa5fd8006b349ed8e973dd48b9002d99d))

- Add script to index documents from Mushpedia JSON into vector store
  ([`78dd265`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/78dd26572d20351f850e4f5b386a12d1aecc49dc))

- Implement RAG chatbot for eMush game with vector store and FastAPI endpoint
  ([`102a65a`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/102a65a85bf7228d4a25a3c2f95d44437d01c8e0))

This commit adds the core implementation of the RAG-powered chatbot for the eMush game, including:

- Vector store management with Chroma - RAG chain for context-aware responses - FastAPI endpoint for
  chat interactions - Logging and error handling - Modular architecture with separate components for
  vector store, RAG chain, and API

The implementation supports: - Semantic document search - Chat history context - Metadata filtering
  - Async processing - Configurable LLM and embedding models

- Implement vector store for document indexing and similarity search using Chroma and OpenAI
  embeddings
  ([`388230a`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/388230af3c5c13928b90b32b8dc66eef92f7a7dc))

### Refactoring

- Modify evaluation script to append results to existing CSV file
  ([`b4e8747`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/b4e8747653abfb5b59f5d9affbbbe00a5cdefb73))

- Remove reformulation step from RAG chain
  ([`2f98805`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/2f988058f1b5ec61d893db5104effbd640601821))

- Enhance question reformulation strategy for RAG retrieval
  ([`c6692ac`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/c6692acdc604c6523b9c8f4959359e7848eababd))

- Remove batch processing from document loading and indexing
  ([`a76d130`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/a76d1303aed22c5f14de37d986645e7000a9495c))

- Remove batch processing in index_documents.py
  ([`4c7e51a`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/4c7e51af8de6e3920dbdb75000924b465ccb1ea9))

- Modify document loading to remove batch return parameter
  ([`25e587f`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/25e587fc3a97ca5ff230203abaeb8de7122e4f0e))

- Remove batch size logic from document loader
  ([`503d418`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/503d418ddae82be86d56489aae1cdb840cc45922))

- Adjust text splitter chunk overlap and remove custom separators
  ([`5d22ca9`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/5d22ca958386e296ee9efc4e9e5b135ca82e47d1))

- Simplify RAG response to return only text response
  ([`51a1845`](https://github.com/cmnemoi/emush_rag_chatbot_poc/commit/51a18453facb49dd4d2a6cf808ad5c759c7e4e06))
