import logging
from typing import List, Dict, Optional
from datetime import datetime
from src.utils import dynamic_import
import pickle
import os

# 新增: 向量庫 minimal 實作
import numpy as np

class SimpleVectorDB:
    def __init__(self):
        self.vectors = []
        self.metadata = []
        self.embedder = None  # 用於查詢時動態載入

    def add(self, vector, meta):
        self.vectors.append(vector)
        self.metadata.append(meta)

    def count(self):
        return len(self.vectors)

    def all(self):
        return list(zip(self.vectors, self.metadata))

    def save(self, path):
        with open(path, "wb") as f:
            pickle.dump({"vectors": self.vectors, "metadata": self.metadata}, f)

    @classmethod
    def load(cls, path):
        db = cls()
        if not os.path.isfile(path):
            return db
        with open(path, "rb") as f:
            data = pickle.load(f)
            db.vectors = data.get("vectors", [])
            db.metadata = data.get("metadata", [])
        return db

    def embed(self, text):
        from src.utils import dynamic_import
        if self.embedder is None:
            SentenceTransformer = dynamic_import("sentence_transformers", "SentenceTransformer")
            self.embedder = SentenceTransformer("BAAI/bge-large-zh-v1.5")  # 可根據 config 調整
        return self.embedder.encode(text)

    def similarity(self, query_vec):
        scores = []
        for v, meta in zip(self.vectors, self.metadata):
            score = float(np.dot(query_vec, v) / (np.linalg.norm(query_vec) * np.linalg.norm(v)))
            scores.append((score, meta))
        scores.sort(reverse=True, key=lambda x: x[0])
        return scores

class RAGIndexer:
    def __init__(self, chroma_db_dir: str, collection_name: str, embedding_model: str, embedding_mode: str = "auto", vector_db_path: str = None):
        self.chroma_db_dir = chroma_db_dir
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.embedding_mode = "manual"  # 強制手動 embedding，避免 llamaindex auto embedding 相依問題
        self.embedder = None
        self.vector_db_path = vector_db_path or os.path.join(chroma_db_dir, f"{collection_name}_vectors.pkl")

        if embedding_mode == "auto":
            HuggingFaceEmbedding = dynamic_import("llama_index.embeddings.huggingface", "HuggingFaceEmbedding")
            if HuggingFaceEmbedding is None:
                raise ImportError("LlamaIndex HuggingFaceEmbedding 無法匯入，請檢查依賴版本")
            self.embedder = HuggingFaceEmbedding(model_name=embedding_model)
            self.vector_db = None
        elif embedding_mode == "manual":
            SentenceTransformer = dynamic_import("sentence_transformers", "SentenceTransformer")
            if SentenceTransformer is None:
                raise ImportError("sentence-transformers 無法匯入，請檢查依賴版本")
            self.embedder = SentenceTransformer(embedding_model)
            self.vector_db = SimpleVectorDB()
        else:
            raise ValueError("embedding_mode 必須為 'auto' 或 'manual'")

    def embed(self, text: str):
        if self.embedding_mode == "auto":
            return self.embedder.get_text_embedding(text)
        elif self.embedding_mode == "manual":
            return self.embedder.encode(text)
        else:
            raise RuntimeError("未知 embedding_mode")

    def index_caption(self, caption_data: Dict) -> bool:
        try:
            emb = self.embed(caption_data["caption"])
        except Exception as e:
            logging.error(f"Embedding 失敗: {e}")
            return False

        if self.embedding_mode == "auto":
            # TODO: LlamaIndex pipeline 寫入
            logging.info(f"[AUTO] Index: {caption_data['image_id']} | emb shape: {getattr(emb, 'shape', None) or len(emb)}")
        elif self.embedding_mode == "manual":
            meta = {
                "image_id": caption_data["image_id"],
                "image_path": caption_data["image_path"],
                "caption": caption_data["caption"],
                "indexed_at": datetime.utcnow().isoformat()
            }
            self.vector_db.add(emb, meta)
            logging.info(f"[MANUAL] Index: {caption_data['image_id']} | emb shape: {getattr(emb, 'shape', None) or len(emb)}")
        return True

    def batch_index(self, caption_list: List[Dict]) -> int:
        success = 0
        for c in caption_list:
            if self.index_caption(c):
                success += 1
        # 持久化 minimal 路徑
        if self.embedding_mode == "manual":
            os.makedirs(self.chroma_db_dir, exist_ok=True)
            self.vector_db.save(self.vector_db_path)
        return success

    def get_collection_stats(self) -> dict:
        if self.embedding_mode == "manual":
            return {"count": self.vector_db.count(), "last_indexed": None}
        else:
            # TODO: LlamaIndex pipeline 統計
            return {"count": 0, "last_indexed": None}
