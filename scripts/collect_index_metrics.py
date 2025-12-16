"""
收集索引指標
"""
import json
import chromadb
from pathlib import Path
from datetime import datetime

def collect_metrics():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    chroma_mode = os.getenv("CHROMA_MODE", "persistent").lower()
    chroma_db_dir = os.getenv("CHROMA_DB_DIR", "vlm-rag-phase1/data/chroma_db")
    chroma_host = os.getenv("CHROMA_DB_HOST", "localhost")
    chroma_port = int(os.getenv("CHROMA_DB_PORT", "8001"))
    collection_name = os.getenv("COLLECTION_NAME", "image_captions")

    if chroma_mode == "http":
        client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
    else:
        client = chromadb.PersistentClient(path=chroma_db_dir)
    collection = client.get_collection(name=collection_name)
    total_count = collection.count()
    log_file = Path("logs/index_log.txt")
    index_time = "Unknown"
    if log_file.exists():
        content = log_file.read_text()
        import re
        time_match = re.search(r"總耗時:\s*([\d.]+)\s*分鐘", content)
        if time_match:
            index_time = f"{time_match.group(1)} 分鐘"
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "total_images": total_count,
        "index_time": index_time,
        "success_rate": f"{total_count}/20",
        "database_path": chroma_db_dir,
        "collection_name": collection_name
    }
    output_path = Path("logs/index_metrics.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    print("\n📊 索引指標:")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    print(f"\n✅ 指標已儲存至: {output_path}")

if __name__ == "__main__":
    collect_metrics()
