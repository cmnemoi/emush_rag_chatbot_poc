from typing import List, Dict, Any
from pathlib import Path
import json
import logging
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
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        
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
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Handle both single document and list of documents
                        if isinstance(data, list):
                            for doc in data:
                                doc['metadata'] = {
                                    'source': doc.get('source', ''),
                                    'link': doc.get('link', '')
                                }
                                documents.append(Document(**doc))
                        else:
                            data['metadata'] = {
                                'source': data.get('source', ''),
                                'link': data.get('link', '')
                            }
                            documents.append(Document(**data))
                            
                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing JSON from {file_path}: {e}")
                except Exception as e:
                    logger.error(f"Error processing document {file_path}: {e}")
                    
            logger.info(f"Successfully loaded {len(documents)} documents")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading documents: {e}")
            return []
