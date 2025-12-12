import os
from typing import List, Dict
from datetime import datetime
from llama_index.core import Document, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from src.config import get_config
from llama_index.core.indices.vector_store import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
# from chromadb.errors import UniqueConstraintViolationError
from tqdm import tqdm

class RAGIndexer:
    def __init__(self, chroma_db_dir: str, collection_name: str, embedding_model: str):
        self.chroma_db_dir = chroma_db_dir
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        config = get_config()
        chroma_host = getattr(config, "CHROMA_DB_HOST", "localhost")
        chroma_port = getattr(config, "CHROMA_DB_PORT", 8001)
        client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        chroma_collection = client.get_or_create_collection(name=collection_name)
        self.vector_store = ChromaVectorStore(
            chroma_collection=chroma_collection,
            collection_name=collection_name
        )
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        self.embed_model = OpenAIEmbedding(model=embedding_model)
        self.index = VectorStoreIndex.from_vector_store(
            self.vector_store,
            storage_context=self.storage_context,
            embed_model=self.embed_model
        )

    def index_caption(self, caption_data: dict) -> bool:
        doc_id = caption_data.get("image_id")
        caption_text = caption_data.get("caption")
        image_path = caption_data.get("image_path")
        try:
            # Check for duplicate
            if self.vector_store._collection.get(ids=[doc_id])["ids"]:
                print(f"[SKIP] Duplicate doc_id: {doc_id}")
                return False  # Skip duplicate
            if not caption_text or not doc_id or not image_path:
                print(f"[ERROR] Missing field: doc_id={doc_id}, caption={caption_text}, image_path={image_path}")
                return False
            doc = Document(
                text=caption_text,
                doc_id=doc_id,
                metadata={
                    "image_id": doc_id,
                    "image_path": image_path,
                    "caption": caption_text,
                    "indexed_at": caption_data.get("timestamp", datetime.utcnow().isoformat(timespec="seconds") + "Z")
                }
            )
            self.index.insert(doc)
            self.vector_store.persist(self.chroma_db_dir)
            return True
        except Exception as e:
            print(f"[EXCEPTION] index_caption failed for doc_id={doc_id}: {e}")
            return False

    def batch_index(self, caption_list: List[dict]) -> int:
        success = 0
        for data in tqdm(caption_list, desc="建立索引"):
            if self.index_caption(data):
                success += 1
        return success

    def get_collection_stats(self) -> dict:
        count = self.vector_store._collection.count()
        return {
            "collection_name": self.collection_name,
            "total_indexed": count
        }
