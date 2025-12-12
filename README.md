# VLM→RAG 圖片自然語言檢索系統（Phase 1）

## 1. 專案介紹
本專案實現靜態圖片的自然語言檢索 MVP，結合 GPT-4V 圖片描述、OpenAI Embedding、Chroma 向量庫與 Streamlit UI，驗證 RAG 技術可行性。

## 2. 快速開始
```bash
git clone <repo>
cd vlm-rag-phase1
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# 填入 OPENAI_API_KEY
```

## 3. 安裝步驟
- Python >= 3.9
- 安裝依賴：`pip install -r requirements.txt`
- 配置 .env，填入 OpenAI API Key

## 4. 使用方式
- 測試圖片放置於 `data/images/`（20 張以上，JPG/PNG）
- 執行索引：`python scripts/index_images.py --image_dir data/images`
- 查詢測試：`python scripts/test_query.py "查詢文字"`
- 啟動 UI：`streamlit run app.py`
- 完整驗證流程見 PHASE1_CHECKLIST.md

## 5. 專案結構
```
vlm-rag-phase1/
├── src/                # 核心模組
├── scripts/            # 執行與驗證腳本
├── data/images/        # 測試圖片
├── data/chroma_db/     # 向量資料庫
├── logs/               # 測試日誌與指標
├── app.py              # Streamlit UI
├── README.md           # 專案說明
├── .env.example        # 環境變數範本
├── requirements.txt    # 依賴清單
```

## 6. 配置說明
`.env` 需包含：
```
OPENAI_API_KEY=sk-...
IMAGE_DIR=data/images
CHROMA_DB_DIR=data/chroma_db
EMBEDDING_MODEL=text-embedding-3-small
VLM_MODEL=gpt-4-vision-preview
COLLECTION_NAME=image_captions
TOP_K=5
```

## 7. 測試與驗證
- 執行 `scripts/check_environment.py`、`scripts/check_images.py` 等輔助腳本
- 索引、查詢、性能、成本、Recall@5 全流程自動化
- 測試報告自動生成：`python scripts/generate_report.py`
- 完成檢查清單：見 PHASE1_CHECKLIST.md

## 8. 常見問題
- API Key 未設置或額度不足
- 測試圖片不足或解析度過低
- 依賴未安裝（請重跑 `pip install -r requirements.txt`）
- 查詢延遲過高（檢查網路與 API 狀態）

## 9. 授權資訊
MIT License

---

**Phase 1 測試報告與驗證流程詳見 PHASE1_TEST_REPORT.md、PHASE1_CHECKLIST.md。**
