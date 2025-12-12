"""
執行完整評估測試
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_query import RAGQuery
from config import get_config

def run_evaluation():
    config = get_config()
    query_engine = RAGQuery(
        chroma_db_dir=config.CHROMA_DB_DIR,
        collection_name=config.COLLECTION_NAME,
        embedding_model=config.EMBEDDING_MODEL
    )
    test_queries = [
        "有人的圖片",
        "有車輛的圖片",
        "室外場景",
        "室內環境",
        "白天的照片",
        "夜晚拍攝的照片",
        "門或入口",
        "建築物"
    ]
    print(f"\n🧪 開始評估測試")
    print(f"{'='*80}")
    print(f"測試查詢數: {len(test_queries)}")
    print(f"每個查詢返回: Top-5")
    print(f"\n{'查詢':<20} {'耗時(秒)':<12} {'結果數':<10} {'最高分':<10} {'最低分'}")
    print(f"{'-'*80}")
    total_time = 0
    results_data = []
    for query_text in test_queries:
        start_time = time.time()
        result = query_engine.query(query_text, top_k=5)
        query_time = time.time() - start_time
        total_time += query_time
        results_data.append({
            "query": query_text,
            "time": query_time,
            "results": result["results"]
        })
        scores = [r["score"] for r in result["results"]]
        max_score = max(scores) if scores else 0
        min_score = min(scores) if scores else 0
        print(f"{query_text:<20} {query_time:>10.2f}s {len(result['results']):>8} {max_score:>9.3f} {min_score:>9.3f}")
    avg_time = total_time / len(test_queries)
    print(f"\n{'='*80}")
    print(f"📊 測試統計")
    print(f"  總耗時: {total_time:.2f} 秒")
    print(f"  平均查詢時間: {avg_time:.2f} 秒")
    print(f"  最快查詢: {min(r['time'] for r in results_data):.2f} 秒")
    print(f"  最慢查詢: {max(r['time'] for r in results_data):.2f} 秒")
    print(f"\n📝 詳細結果已儲存至 logs/evaluation_results.txt")
    with open("logs/evaluation_results.txt", "w", encoding="utf-8") as f:
        f.write("# Phase 1 評估測試結果\n\n")
        for data in results_data:
            f.write(f"## 查詢: {data['query']}\n")
            f.write(f"查詢時間: {data['time']:.2f} 秒\n\n")
            f.write("### Top-5 結果:\n")
            for i, res in enumerate(data['results'], 1):
                f.write(f"{i}. [分數: {res['score']:.3f}]\n")
                f.write(f"   圖片: {res['image_path']}\n")
                f.write(f"   描述: {res['caption']}\n")
                f.write(f"   相關性: [ ] 相關  [ ] 不相關 （請人工勾選）\n\n")
            f.write(f"{'-'*80}\n\n")
    print(f"\n✅ 評估完成！")
    print(f"\n下一步:")
    print(f"1. 開啟 logs/evaluation_results.txt")
    print(f"2. 對每個結果標記是否相關")
    print(f"3. 計算 Recall@5\n")

if __name__ == "__main__":
    Path("logs").mkdir(exist_ok=True)
    run_evaluation()
