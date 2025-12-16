import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    OPENAI_API_KEY: str
    IMAGE_DIR: str
    CHROMA_DB_DIR: str
    COLLECTION_NAME: str
    EMBEDDING_MODEL: str
    VLM_MODEL: str
    TOP_K: int
    EMBEDDING_MODE: str  # "auto" or "manual"

def get_config() -> Config:
    return Config(
        OPENAI_API_KEY=os.getenv("OPENAI_API_KEY", ""),
        IMAGE_DIR=os.getenv("IMAGE_DIR", "data/images"),
        CHROMA_DB_DIR=os.getenv("CHROMA_DB_DIR", "data/chroma_db"),
        COLLECTION_NAME=os.getenv("COLLECTION_NAME", "image_captions"),
        EMBEDDING_MODEL=os.getenv("EMBEDDING_MODEL", "BAAI/bge-large-zh-v1.5"),
        VLM_MODEL=os.getenv("VLM_MODEL", "gpt-4-vision-preview"),
        TOP_K=int(os.getenv("TOP_K", "5")),
        EMBEDDING_MODE=os.getenv("EMBEDDING_MODE", "auto"),  # 新增
    )
