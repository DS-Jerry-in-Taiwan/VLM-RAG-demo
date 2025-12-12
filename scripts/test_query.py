import argparse
from src.config import get_config
from src.rag_query import RAGQuery

def print_results(result: dict):
    print(f"\n[查詢] {result['query']}\n")
    print(f"[結果] 找到 {len(result['results'])} 張相關圖片 (查詢時間: {result['query_time']}秒)\n")
    for idx, item in enumerate(result["results"], 1):
        print(f"{idx}. [分數: {item['score']:.2f}]")
        print(f"   圖片: {item['image_path']}")
        print(f"   描述: {item['caption']}\n")

def interactive_mode(rag: RAGQuery):
    print("進入互動模式，輸入查詢文字（輸入 exit 離開）")
    while True:
        query = input("查詢: ").strip()
        if query.lower() in ("exit", "quit"):
            break
        result = rag.query(query)
        print_results(result)

def main():
    parser = argparse.ArgumentParser(description="RAG 查詢測試")
    parser.add_argument("query", nargs="?", type=str, help="查詢文字")
    parser.add_argument("--interactive", action="store_true", help="互動模式")
    args = parser.parse_args()

    config = get_config()
    rag = RAGQuery(
        chroma_db_dir=config.CHROMA_DB_DIR,
        collection_name=config.COLLECTION_NAME,
        embedding_model=config.EMBEDDING_MODEL
    )

    if args.interactive:
        interactive_mode(rag)
    elif args.query:
        result = rag.query(args.query)
        print_results(result)
    else:
        print("請輸入查詢文字或使用 --interactive 進入互動模式")

if __name__ == "__main__":
    main()
