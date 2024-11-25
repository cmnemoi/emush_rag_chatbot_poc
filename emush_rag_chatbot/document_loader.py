import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Document(BaseModel):
    """Schema for eMush game documentation"""

    title: str
    link: str
    source: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DocumentLoader:
    """Loads and processes eMush game documentation from JSON files"""

    def __init__(self, data_dir: str = "data", chunk_size: int = 10_000, chunk_overlap: int = 100):
        self.data_dir = Path(data_dir)
        self.chunk_size = chunk_size
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    def load_documents(self) -> List[Document]:
        """
        Load JSON documents from the data directory

        Returns:
            List[Document]: List of parsed game documentation
        """
        try:
            json_files = list(self.data_dir.glob("*.json"))
            if not json_files:
                logger.warning(f"No JSON files found in {self.data_dir}")
                return []

            documents = []
            for file_path in json_files:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        # Handle both single document and list of documents
                        if isinstance(data, list):
                            for doc in data:
                                metadata = {
                                    "source": doc.get("source", ""),
                                    "link": doc.get("link", ""),
                                    "title": doc.get("title", ""),
                                }
                                # Split long documents
                                if len(doc["content"]) > self.chunk_size:
                                    splits = self.text_splitter.split_text(doc["content"])
                                    for i, split_content in enumerate(splits):
                                        split_doc = doc.copy()
                                        split_doc["content"] = split_content
                                        split_doc["metadata"] = {**metadata, "chunk": i, "total_chunks": len(splits)}
                                        documents.append(Document(**split_doc))
                                else:
                                    documents.append(Document(**doc))
                        else:
                            metadata = {
                                "source": data.get("source", ""),
                                "link": data.get("link", ""),
                                "title": data.get("title", ""),
                            }
                            # Split long documents
                            if len(data["content"]) > self.chunk_size:
                                splits = self.text_splitter.split_text(data["content"])
                                for i, split_content in enumerate(splits):
                                    split_doc = data.copy()
                                    split_doc["content"] = split_content
                                    split_doc["metadata"] = {**metadata, "chunk": i, "total_chunks": len(splits)}
                                    documents.append(Document(**split_doc))
                            else:
                                documents.append(Document(**split_doc))

                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing JSON from {file_path}: {e}")
                except Exception as e:
                    logger.error(f"Error processing document {file_path}: {e}")

            logger.info(f"Successfully loaded {len(documents)} documents")
            return documents

        except Exception as e:
            logger.error(f"Error loading documents: {e}")
            return []
