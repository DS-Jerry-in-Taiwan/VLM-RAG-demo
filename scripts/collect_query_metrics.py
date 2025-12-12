"""
收集查詢指標
"""
import json
import re
from pathlib import Path
from datetime import datetime

def parse_query_log():
    log_file = Path("logs/query_log.txt")
    if not log_file.exists():
        print("❌ 查詢日誌不存在")
        return None
    content = log_file.read_text()
    query_times = []
    for line in content.split('\n'):
        match = re.search(r'(\d+\.\d+)s', line)
        if match:
            query_times.append(float(match.group(1)))
    if not query_times:
        return None
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "total_queries": len(query_times),
        "avg_query_time": sum(query_times) / len(query_times),
        "min_query_time": min(query_times),
        "max_query_time": max(query_times),
        "all_query_times": query_times
    }
    return metrics

def main():
    metrics = parse_query_log()
    if metrics:
        output_path = Path("logs/query_metrics.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)
        print("\n📊 查詢指標:")
        print(f"  總查詢數: {metrics['total_queries']}")
        print(f"  平均時間: {metrics['avg_query_time']:.2f} 秒")
        print(f"  最快: {metrics['min_query_time']:.2f} 秒")
        print(f"  最慢: {metrics['max_query_time']:.2f} 秒")
        print(f"\n✅ 指標已儲存至: {output_path}")
        if metrics['avg_query_time'] < 2.0:
            print("\n✅ 查詢延遲符合目標 (< 2秒)")
        else:
            print(f"\n⚠️  查詢延遲超過目標: {metrics['avg_query_time']:.2f}s > 2.0s")
    else:
        print("❌ 無法解析查詢日誌")

if __name__ == "__main__":
    main()
