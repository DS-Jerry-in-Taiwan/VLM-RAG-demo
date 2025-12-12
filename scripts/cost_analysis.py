"""
API 成本分析
"""
def analyze_costs():
    num_images = 20
    avg_caption_tokens = 50
    gpt4v_price = 0.01
    embedding_price = 0.00002
    vlm_cost = num_images * gpt4v_price
    embedding_cost = (num_images * avg_caption_tokens / 1000) * embedding_price
    query_cost = 0.0001
    total_cost = vlm_cost + embedding_cost + query_cost
    print(f"\n💰 API 成本分析")
    print(f"{'='*50}")
    print(f"圖片數量: {num_images}")
    print(f"\n費用明細:")
    print(f"  GPT-4V (Caption 生成): ${vlm_cost:.4f}")
    print(f"  Embedding (索引):      ${embedding_cost:.4f}")
    print(f"  Embedding (查詢):      ${query_cost:.4f}")
    print(f"{'-'*50}")
    print(f"  總計:                  ${total_cost:.4f}")
    print(f"\n{'='*50}")
    if total_cost < 1.0:
        print(f"✅ 成本控制良好（< $1）")
    else:
        print(f"⚠️  成本超出預算")
    print(f"\n📈 擴展性預估:")
    for scale in [20, 100, 1000]:
        scaled_cost = (vlm_cost / num_images) * scale
        print(f"  {scale:>5} 張圖片: ${scaled_cost:>8.2f}")
    print(f"\n💡 成本優化建議:")
    print(f"  - Phase 2 改用開源 VLM (Qwen2-VL) 可降低 90% 成本")
    print(f"  - Batch processing 可提升 30% 效率\n")

if __name__ == "__main__":
    analyze_costs()
