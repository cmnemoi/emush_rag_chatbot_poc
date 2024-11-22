from pathlib import Path
from pydantic_settings import BaseSettings  # type: ignore


class Settings(BaseSettings):
    """Application settings"""

    # Project paths
    BASE_DIR: Path = Path(__file__).parent
    DATA_DIR: Path = BASE_DIR / "data"

    # OpenAI settings
    OPENAI_API_KEY: str = ""

    # Vector store settings
    CHROMA_PERSIST_DIR: Path = BASE_DIR / "chroma_db"

    # Model settings
    EMBEDDING_MODEL: str = "text-embedding-3-large"
    CHAT_MODEL: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"


settings = Settings()
