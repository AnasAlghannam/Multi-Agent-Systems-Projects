from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import MAX_FILE_SIZE, MAX_TOTAL_SIZE, ALLOWED_TYPES


class Settings(BaseSettings):
    """Application settings, overridable through .env or the environment."""

    # Upload limits
    MAX_FILE_SIZE: int = MAX_FILE_SIZE
    MAX_TOTAL_SIZE: int = MAX_TOTAL_SIZE
    ALLOWED_TYPES: list = ALLOWED_TYPES

    # Vector store
    CHROMA_DB_PATH: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "documents"

    # Retrieval
    # Local sentence-transformers model; downloaded once, then cached.
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    VECTOR_SEARCH_K: int = 10
    # Blend of [BM25 keyword, vector semantic] scores.
    HYBRID_RETRIEVER_WEIGHTS: list = [0.4, 0.6]

    # Logging
    LOG_LEVEL: str = "INFO"

    # Parsed-document cache
    CACHE_DIR: str = "document_cache"
    CACHE_EXPIRE_DAYS: int = 7

    # extra="ignore" matters: the .env also holds credentials such as
    # GROQ_API_KEY that are read directly by the model client. Without it,
    # pydantic rejects them as unexpected fields - and echoes their values into
    # the traceback, which would leak the key into logs.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
