import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError, Field

class Config(BaseModel):
    OPENAI_API_KEY: str = Field(..., description="OpenAI API Key")
    IMAGE_DIR: str = Field(..., description="Directory for images")
    CHROMA_DB_DIR: str = Field(..., description="Directory for Chroma DB")
    CHROMA_DB_HOST: str = Field("localhost", description="ChromaDB host")
    CHROMA_DB_PORT: int = Field(8001, description="ChromaDB port")
    COLLECTION_NAME: str = Field(..., description="Chroma collection name")
    EMBEDDING_MODEL: str = Field(..., description="Embedding model name")
    VLM_MODEL: str = Field(..., description="VLM model name")
    TOP_K: int = Field(5, description="Top K results to return")

def get_config(env_path: Optional[str] = None) -> Config:
    """
    Load configuration from .env file and environment variables.
    Raises ValidationError if required config is missing.
    """
    if env_path:
        load_dotenv(env_path)
    else:
        load_dotenv()
    # Gather all required variables
    env_vars = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "IMAGE_DIR": os.getenv("IMAGE_DIR"),
        "CHROMA_DB_DIR": os.getenv("CHROMA_DB_DIR"),
        "CHROMA_DB_HOST": os.getenv("CHROMA_DB_HOST", "localhost"),
        "CHROMA_DB_PORT": os.getenv("CHROMA_DB_PORT", "8001"),
        "COLLECTION_NAME": os.getenv("COLLECTION_NAME"),
        "EMBEDDING_MODEL": os.getenv("EMBEDDING_MODEL"),
        "VLM_MODEL": os.getenv("VLM_MODEL"),
        "TOP_K": os.getenv("TOP_K", "5"),
    }
    missing = [k for k, v in env_vars.items() if v is None]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")
    try:
        config = Config(
            OPENAI_API_KEY=env_vars["OPENAI_API_KEY"],
            IMAGE_DIR=env_vars["IMAGE_DIR"],
            CHROMA_DB_DIR=env_vars["CHROMA_DB_DIR"],
            CHROMA_DB_HOST=env_vars["CHROMA_DB_HOST"],
            CHROMA_DB_PORT=int(env_vars["CHROMA_DB_PORT"]),
            COLLECTION_NAME=env_vars["COLLECTION_NAME"],
            EMBEDDING_MODEL=env_vars["EMBEDDING_MODEL"],
            VLM_MODEL=env_vars["VLM_MODEL"],
            TOP_K=int(env_vars["TOP_K"]),
        )
    except ValidationError as e:
        raise RuntimeError(f"Config validation error: {e}")
    return config
