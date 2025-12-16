import logging
import time
from typing import List, Dict, Optional
from src.utils import dynamic_import

class RAGQuery:
    def __init__(
        self,
        chroma_db_dir: str,
        collection_name: str,
        embedding_model: str,
        embedding_mode: str = "auto",
        vector_db=None,
        chroma_http_host: Optional[str] = None,
        chroma_http_port: Optional[str] = None,
    ):
        self.chroma_db_dir = chroma_db_dir
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.embedding_mode = embedding_mode
        self.vector_db = vector_db
        self.chroma_http_host = chroma_http_host
        self.chroma_http_port = chroma_http_port

        if embedding_mode == "auto":
            # 支援 docker http chromadb
            chroma_kwargs = {}
            if chroma_http_host and chroma_http_port:
                chroma_kwargs["host"] = chroma_http_host
                chroma_kwargs["port"] = int(chroma_http_port)
                chroma_kwargs["ssl"] = False
                chroma_kwargs["persist_directory"] = None
            else:
                chroma_kwargs["persist_directory"] = chroma_db_dir

            ChromaVectorStore = dynamic_import("llama_index.vector_stores.chroma", "ChromaVectorStore")
            if ChromaVectorStore is None:
                raise ImportError("ChromaVectorStore 無法匯入，請檢查依賴版本")
            self.chroma_vs = ChromaVectorStore(
                collection_name=collection_name,
                **chroma_kwargs
            )
            HuggingFaceEmbedding = dynamic_import("llama_index.embeddings.huggingface", "HuggingFaceEmbedding")
            if HuggingFaceEmbedding is None:
                raise ImportError("LlamaIndex HuggingFaceEmbedding 無法匯入，請檢查依賴版本")
            self.embedder = HuggingFaceEmbedding(model_name=embedding_model)
        elif embedding_mode == "manual":
            from src.rag_indexer import SimpleVectorDB
            import os
            vector_db_path = os.path.join(chroma_db_dir, f"{collection_name}_vectors.pkl")
            self.vector_db = SimpleVectorDB.load(vector_db_path)
            self.embedder = None  # minimal 路徑由 vector_db 提供
        else:
            raise ValueError("embedding_mode 必須為 'auto' 或 'manual'")

    def query(self, query_text: str, top_k: int = 5) -> Dict:
        t0 = time.time()
        if self.embedding_mode == "auto":
            query_vec = self.embedder.get_text_embedding(query_text)
            results = self.chroma_vs.similarity_search(query_vec, top_k=top_k)
            out = []
            for r in results:
                out.append({
                    "image_id": r.metadata.get("image_id"),
                    "image_path": r.metadata.get("image_path"),
                    "caption": r.metadata.get("caption"),
                    "score": r.score,
                })
        elif self.embedding_mode == "manual":
            # minimal 路徑
            if not self.vector_db:
                return {"query": query_text, "results": [], "query_time": 0}
            query_vec = self.vector_db.embed(query_text)
            sims = self.vector_db.similarity(query_vec)
            out = []
            for idx, (score, meta) in enumerate(sims[:top_k]):
                out.append({
                    "image_id": meta["image_id"],
                    "image_path": meta["image_path"],
                    "caption": meta["caption"],
                    "score": float(score),
                })
        else:
            out = []
        t1 = time.time()
        return {
            "query": query_text,
            "results": out,
            "query_time": round(t1 - t0, 3)
        }
