from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


#Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    github_token: str = ""

    openai_api_key: str = ""

    default_repository: str = ""

    embedding_model: str = "all-MiniLM-L6-v2"
    llm_model: str = "gpt-6-luna"

    chroma_collection_name: str = "commitsage"

    top_k: int = 10

    rerank_top_k: int = 5

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()


#Important project directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EVALUATION_DATA_DIR = DATA_DIR / "evaluation"

MODELS_DIR = PROJECT_ROOT / "models"
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"

