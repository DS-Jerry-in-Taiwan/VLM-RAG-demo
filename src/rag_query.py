import time
from typing import List, Dict
from llama_index.core.indices.vector_store import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding

class RAGQuery:
    def __init__(self, chroma_db_dir: str, collection_name: str, embedding_model: str):
        self.vector_store = ChromaVectorStore(
            collection_name=collection_name,
            host="localhost",
            port=8001
        )
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        self.embed_model = OpenAIEmbedding(model=embedding_model)
        self.index = VectorStoreIndex.from_vector_store(
            self.vector_store,
            storage_context=self.storage_context,
            embed_model=self.embed_model
        )
        self.query_engine = self.index.as_query_engine(similarity_top_k=5)

    def query(self, query_text: str, top_k: int = 5) -> dict:
        start = time.time()
        results = self.query_engine.query(query_text)
        elapsed = round(time.time() - start, 2)
        output = {
            "query": query_text,
            "results": [],
            "query_time": elapsed
        }
        # results is a list of NodeWithScore objects
        for node in getattr(results, "nodes", [])[:top_k]:
            meta = getattr(node, "metadata", {}) or {}
            output["results"].append({
                "image_id": meta.get("image_id", ""),
                "image_path": meta.get("image_path", ""),
                "caption": meta.get("caption", ""),
                "score": getattr(node, "score", 0)
            })
        return output

    def get_image_by_id(self, image_id: str) -> dict:
        docs = self.vector_store._collection.get(ids=[image_id])
        if docs and docs.get("ids"):
            metadatas = docs.get("metadatas")
            if metadatas and len(metadatas) > 0:
                meta = metadatas[0]
                return {
                    "image_id": meta.get("image_id", ""),
                    "image_path": meta.get("image_path", ""),
                    "caption": meta.get("caption", "")
                }
        return {}
