"""
自動生成 Phase 1 測試報告
"""
import json
from pathlib import Path
from datetime import datetime
import sys
import platform

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def generate_report():
    index_metrics = load_json("logs/index_metrics.json")
    query_metrics = load_json("logs/query_metrics.json")
    recall_metrics = load_json("logs/recall_metrics.json")
    performance = load_json("logs/performance_analysis.json")
    overall_recall = recall_metrics.get('overall_recall', 0)
    avg_time = query_metrics.get('avg_query_time', 0)
    total_cost = performance.get('cost_analysis', {}).get('total_cost', 0)
    decision = performance.get('decision', 'UNKNOWN')
    report = f"""# Phase 1 測試報告

**生成時間：** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

***

## 一、執行摘要

### 測試概況
- **測試日期：** {datetime.now().strftime("%Y-%m-%d")}
- **測試圖片數：** {index_metrics.get('total_images', 'N/A')}
- **測試查詢數：** {query_metrics.get('total_queries', 'N/A')}

### 整體結論
"""
    if decision == "GO":
        report += "✅ **Phase 1 測試通過！建議繼續 Phase 2 開發。**\n\n"
    else:
        report += "⚠️ **Phase 1 測試部分未通過，建議優化後重測。**\n\n"
    report += """### 指標檢查

| 指標 | 目標 | 實際 | 狀態 |
|------|------|------|------|
"""
    report += f"| Recall@5 | > 0.70 | {overall_recall:.2%} | {'✅' if overall_recall > 0.70 else '❌'} |\n"
    report += f"| 查詢延遲 | < 2s | {avg_time:.2f}s | {'✅' if avg_time < 2.0 else '❌'} |\n"
    report += f"| API 成本 | < $1 | ${total_cost:.4f} | {'✅' if total_cost < 1.0 else '❌'} |\n"
    report += f"| 索引成功 | 20 張 | {index_metrics.get('total_images', 0)} 張 | {'✅' if index_metrics.get('total_images', 0) >= 20 else '❌'} |\n\n"
    report += f"""---

## 二、詳細測試結果

### 2.1 索引測試

- **索引時間：** {index_metrics.get('index_time', 'N/A')}
- **圖片數量：** {index_metrics.get('total_images', 'N/A')}
- **成功率：** {index_metrics.get('success_rate', 'N/A')}

### 2.2 查詢測試

- **總查詢數：** {query_metrics.get('total_queries', 'N/A')}
- **平均延遲：** {avg_time:.2f} 秒
- **最快/最慢：** {query_metrics.get('min_query_time', 0):.2f}s / {query_metrics.get('max_query_time', 0):.2f}s

### 2.3 Recall@5 評估

- **Overall Recall@5：** {overall_recall:.2%}
- **通過標準：** {'✅ 是' if overall_recall > 0.70 else '❌ 否'}

"""
    if recall_metrics.get('queries'):
        report += "#### 各查詢 Recall 明細\n\n"
        report += "| 查詢 | 相關數/總數 | Recall |\n"
        report += "|------|------------|--------|\n"
        for q in recall_metrics.get('queries', []):
            report += f"| {q.get('query', 'N/A')} | {q.get('relevant_count', 0)}/{q.get('total_count', 5)} | {q.get('recall', 0):.2%} |\n"
        report += "\n"
    report += f"""### 2.4 成本分析

- **總計：** ${total_cost:.4f}
- **通過標準：** {'✅ 是' if total_cost < 1.0 else '❌ 否'}

***

## 三、發現的問題

（請手動補充測試過程中發現的問題）

***

## 四、改進建議

### 4.1 短期優化（Phase 1 迭代）

1. VLM Prompt 優化
2. 測試資料多樣性提升
3. 查詢優化

### 4.2 中長期優化（Phase 2）

1. 改用開源 VLM (Qwen2-VL-7B)
2. 結構化欄位提取
3. 混合檢索
4. Reranking

***

## 五、Phase 2 建議

### 5.1 Go/No-Go 決策

"""
    if decision == "GO":
        report += "**決策：GO - 繼續 Phase 2 開發**\n\n"
    else:
        report += "**決策：NO-GO - Phase 1 迭代優化**\n\n"
    report += """### 5.2 Phase 2 優先級

| 優先級 | 任務 | 理由 |
|--------|------|------|
| P0 | 整合 Qwen2-VL | 降低成本 |
| P0 | 結構化欄位提取 | 支援混合檢索 |
| P1 | 升級向量庫 (Milvus) | 支援大規模 |
| P1 | Reranker 整合 | 提升精確度 |

***

## 六、附錄

### 6.1 測試環境

- **Python 版本：** {sys.version.split()[0]}
- **作業系統：** {platform.system()}

### 6.2 相關檔案

- 索引日誌：`logs/index_log.txt`
- 查詢日誌：`logs/query_log.txt`
- 評估結果：`logs/evaluation_results.txt`
- 性能分析：`logs/performance_analysis.json`

***

**報告結束**
"""
    output_path = Path("PHASE1_TEST_REPORT.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n✅ 測試報告已生成: {output_path}\n")

if __name__ == "__main__":
    generate_report()
