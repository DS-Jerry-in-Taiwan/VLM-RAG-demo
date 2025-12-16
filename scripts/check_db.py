"""
檢查 Chroma 資料庫狀態
"""
import chromadb
from pathlib import Path
import sys

def check_database(collection_name: str):
    import os
    from dotenv import load_dotenv
    load_dotenv()
    chroma_mode = os.getenv("CHROMA_MODE", "persistent").lower()
    chroma_db_dir = os.getenv("CHROMA_DB_DIR", "vlm-rag-phase1/data/chroma_db")
    chroma_host = os.getenv("CHROMA_DB_HOST", "localhost")
    chroma_port = int(os.getenv("CHROMA_DB_PORT", "8001"))

    try:
        if chroma_mode == "http":
            client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        else:
            client = chromadb.PersistentClient(path=chroma_db_dir)
        collections = client.list_collections()
        if collection_name not in [c.name for c in collections]:
            print(f"❌ Collection {collection_name} 不存在於 ChromaDB")
            return False
        collection = client.get_collection(name=collection_name)
        count = collection.count()
        print(f"\n📊 Chroma 資料庫狀態")
        print(f"{'='*50}")
        print(f"Collection: {collection_name}")
        print(f"索引數量: {count}")
        if count > 0:
            sample = collection.peek(limit=3)
            print(f"\n📝 前 3 筆資料範例：")
            ids = sample.get('ids') or []
            metadatas = sample.get('metadatas') or []
            for i in range(min(len(ids), len(metadatas))):
                doc_id = ids[i]
                metadata = metadatas[i]
                print(f"\n{i+1}. ID: {doc_id}")
                print(f"   Caption: {metadata.get('caption', 'N/A')[:50]}...")
                print(f"   Image: {metadata.get('image_path', 'N/A')}")
        print(f"\n✅ 資料庫健康")
        return True
    except Exception as e:
        print(f"❌ 資料庫錯誤: {e}")
        return False

if __name__ == "__main__":
    collection_name = sys.argv[1] if len(sys.argv) > 1 else "image_captions"
    success = check_database(collection_name)
    sys.exit(0 if success else 1)
