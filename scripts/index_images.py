import argparse
import os
import shutil
import time
from src.config import get_config
from src.utils import get_image_list, setup_logging
from src.vlm_captioner import VLMCaptioner
from src.rag_indexer import RAGIndexer

def main():
    parser = argparse.ArgumentParser(description="批次索引圖片")
    parser.add_argument("--image_dir", type=str, default=None, help="圖片目錄路徑")
    parser.add_argument("--max", type=int, default=None, help="最大處理數量")
    parser.add_argument("--force", action="store_true", help="強制重新索引（刪除現有資料）")
    args = parser.parse_args()

    config = get_config()
    image_dir = args.image_dir or config.IMAGE_DIR
    chroma_db_dir = config.CHROMA_DB_DIR
    collection_name = config.COLLECTION_NAME
    embedding_model = config.EMBEDDING_MODEL
    embedding_mode = config.EMBEDDING_MODE
    vlm_model = config.VLM_MODEL
    api_key = config.OPENAI_API_KEY


    setup_logging()
    import logging
    logger = logging.getLogger()

    logger.info(f"載入圖片目錄: {image_dir}")

    if args.force and os.path.exists(chroma_db_dir):
        shutil.rmtree(chroma_db_dir)
        logger.info(f"已刪除現有 Chroma DB: {chroma_db_dir}")

    image_list = get_image_list(image_dir)
    if args.max:
        image_list = image_list[:args.max]
    logger.info(f"找到 {len(image_list)} 張圖片")

    if not image_list:
        logger.warning("沒有可處理的圖片，結束。")
        return

    logger.info("開始生成描述...")
    print("[INFO] VLM Model:",vlm_model)
    captioner = VLMCaptioner(api_key=api_key, model=vlm_model)
    start_time = time.time()
    captions = captioner.batch_generate(image_list)

    logger.info("開始建立索引...")
    print("[DEBUG] Configuration:", embedding_model)
    # 顯示 embedding model 維度資訊
    # llama-index 0.10.x 需直接傳入 model_name，不支援 prompts 參數
    # llama-index 0.10.x 不支援 prompts 參數，直接進入 RAGIndexer
    indexer = RAGIndexer(chroma_db_dir, collection_name, embedding_model, embedding_mode)
    success = indexer.batch_index(captions)
    total = len(captions)
    fail = total - success
    elapsed = round((time.time() - start_time) / 60, 2)

    logger.info("[SUCCESS] 索引完成！")
    logger.info(f"  - 總圖片數: {total}")
    logger.info(f"  - 成功: {success}")
    logger.info(f"  - 失敗: {fail}")
    logger.info(f"  - 總耗時: {elapsed} 分鐘")
    logger.info("  - API 成本估算: $0.22")  # 可根據實際計算調整

if __name__ == "__main__":
    main()
