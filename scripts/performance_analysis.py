"""
綜合性能分析
"""
import json
from pathlib import Path
from datetime import datetime

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def main():
    print("\n" + "=" * 60)
    print("📊 Phase 1 綜合性能分析")
    print("=" * 60)
    index_metrics = load_json("logs/index_metrics.json")
    query_metrics = load_json("logs/query_metrics.json")
    recall_metrics = load_json("logs/recall_metrics.json")
    # 索引性能
    if index_metrics:
        print("\n### 索引性能")
        print(f"  圖片數量: {index_metrics.get('total_images', 'N/A')}")
        print(f"  索引時間: {index_metrics.get('index_time', 'N/A')}")
        print(f"  成功率: {index_metrics.get('success_rate', 'N/A')}")
    # 查詢性能
    if query_metrics:
        print("\n### 查詢性能")
        print(f"  總查詢數: {query_metrics.get('total_queries', 'N/A')}")
        print(f"  平均時間: {query_metrics.get('avg_query_time', 0):.2f} 秒")
        avg_time = query_metrics.get('avg_query_time', 999)
        if avg_time < 2.0:
            print("  ✅ 符合目標 (< 2秒)")
        else:
            print(f"  ❌ 超過目標 ({avg_time:.2f}s > 2.0s)")
    # Recall 評估
    if recall_metrics:
        print("\n### Recall@5 評估")
        overall_recall = recall_metrics.get('overall_recall', 0)
        print(f"  Overall Recall@5: {overall_recall:.2%}")
        if overall_recall > 0.70:
            print("  ✅ 符合目標 (> 70%)")
        else:
            print(f"  ❌ 未達目標 ({overall_recall:.2%} < 70%)")
    # 成本估算
    print("\n### 成本估算")
    num_images = index_metrics.get('total_images', 20) if index_metrics else 20
    total_cost = num_images * 0.01 + 0.0001
    print(f"  總計: ${total_cost:.4f}")
    if total_cost < 1.0:
        print("  ✅ 符合預算 (< $1)")
    else:
        print(f"  ⚠️  超出預算 (${total_cost:.4f} > $1)")
    # 整體判斷
    print("\n" + "=" * 60)
    print("### 整體評估")
    checks = {
        "Recall@5 > 0.70": recall_metrics.get('overall_recall', 0) > 0.70 if recall_metrics else False,
        "查詢延遲 < 2s": query_metrics.get('avg_query_time', 999) < 2.0 if query_metrics else False,
        "成本 < $1": total_cost < 1.0,
        "索引成功": index_metrics.get('total_images', 0) >= 20 if index_metrics else False
    }
    passed = sum(checks.values())
    total = len(checks)
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check_name}")
    print(f"\n通過率: {passed}/{total} ({passed/total*100:.0f}%)")
    if passed >= 3:
        print("\n✅ Phase 1 測試通過！建議繼續 Phase 2")
        decision = "GO"
    else:
        print("\n⚠️  Phase 1 測試未完全通過，建議優化後重測")
        decision = "NO-GO"
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "index_metrics": index_metrics,
        "query_metrics": query_metrics,
        "recall_metrics": recall_metrics,
        "cost_analysis": {"total_cost": total_cost},
        "checks": checks,
        "passed_count": passed,
        "total_count": total,
        "decision": decision
    }
    output_path = Path("logs/performance_analysis.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    print(f"\n✅ 分析結果已儲存至: {output_path}")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
