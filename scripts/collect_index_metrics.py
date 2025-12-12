"""
收集索引指標
"""
import json
import chromadb
from pathlib import Path
from datetime import datetime

def collect_metrics():
    client = chromadb.PersistentClient(path="data/chroma_db")
    collection = client.get_collection(name="image_captions")
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
        "database_path": "data/chroma_db",
        "collection_name": "image_captions"
    }
    output_path = Path("logs/index_metrics.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    print("\n📊 索引指標:")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    print(f"\n✅ 指標已儲存至: {output_path}")

if __name__ == "__main__":
    collect_metrics()
