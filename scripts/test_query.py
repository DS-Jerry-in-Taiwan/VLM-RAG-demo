import argparse
from src.config import get_config
from src.rag_query import RAGQuery
import logging
import os

def main():
    parser = argparse.ArgumentParser(description="查詢測試腳本")
    parser.add_argument("query", type=str, nargs="?", help="查詢文字")
    parser.add_argument("--top_k", type=int, default=None, help="返回 top_k 結果")
    args = parser.parse_args()

    config = get_config()
    chroma_db_dir = config.CHROMA_DB_DIR
    collection_name = config.COLLECTION_NAME
    embedding_model = config.EMBEDDING_MODEL
    embedding_mode = config.EMBEDDING_MODE
    top_k = args.top_k or config.TOP_K

    # docker http 服務模式
    chroma_mode = os.getenv("CHROMA_MODE", "persistent")
    chroma_host = os.getenv("CHROMA_DB_HOST", "localhost")
    chroma_port = os.getenv("CHROMA_DB_PORT", "8001")

    rag_kwargs = {}
    if embedding_mode == "auto" and chroma_mode == "http":
        rag_kwargs["chroma_http_host"] = chroma_host
        rag_kwargs["chroma_http_port"] = chroma_port

    rag = RAGQuery(
        chroma_db_dir=chroma_db_dir,
        collection_name=collection_name,
        embedding_model=embedding_model,
        embedding_mode=embedding_mode,
        **rag_kwargs
    )

    if not args.query:
        print("請輸入查詢文字")
        return

    result = rag.query(args.query, top_k=top_k)
    print(f"[查詢] {result['query']}\n")
    print(f"[結果] 找到 {len(result['results'])} 張相關圖片 (查詢時間: {result['query_time']}秒)\n")
    for i, r in enumerate(result["results"], 1):
        print(f"{i}. [分數: {r['score']}]")
        print(f"   圖片: {r['image_path']}")
        print(f"   描述: {r['caption']}\n")

if __name__ == "__main__":
    main()
