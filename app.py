import streamlit as st
from src.config import get_config
from src.utils import setup_logging
from src.vlm_captioner import VLMCaptioner
from src.rag_indexer import RAGIndexer
from src.rag_query import RAGQuery
import os
import time

st.set_page_config(page_title="VLM→RAG 圖片檢索系統", layout="wide")
setup_logging()

config = get_config()
image_dir = config.IMAGE_DIR
chroma_db_dir = config.CHROMA_DB_DIR
collection_name = config.COLLECTION_NAME
embedding_model = config.EMBEDDING_MODEL
vlm_model = config.VLM_MODEL
api_key = config.OPENAI_API_KEY

st.title("VLM→RAG 圖片檢索系統")

tab1, tab2 = st.tabs(["索引管理", "查詢介面"])

with tab1:
    st.header("索引管理")
    uploaded_files = st.file_uploader("上傳圖片", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            save_path = os.path.join(image_dir, file.name)
            with open(save_path, "wb") as f:
                f.write(file.getbuffer())
        st.success(f"已上傳 {len(uploaded_files)} 張圖片")

    if st.button("開始索引"):
        st.info("開始生成描述與建立索引...")
        print("[INFO] Starting indexing process-------",vlm_model)
        captioner = VLMCaptioner(api_key=api_key, model=vlm_model)
        indexer = RAGIndexer(chroma_db_dir, collection_name, embedding_model)
        image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir)
                       if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        captions = captioner.batch_generate(image_files)
        indexer.batch_index(captions)
        st.success("索引完成！")

    indexer = RAGIndexer(chroma_db_dir, collection_name, embedding_model)
    stats = indexer.get_collection_stats()
    st.write(f"總圖片數: {stats['total_indexed']}")
    st.write(f"最後索引時間: {time.strftime('%Y-%m-%d %H:%M:%S')}")

with tab2:
    st.header("查詢介面")
    query_text = st.text_input("請輸入查詢文字")
    top_k = st.number_input("返回圖片數量 Top-K", min_value=1, max_value=10, value=5)
    if st.button("搜尋") and query_text:
        rag = RAGQuery(chroma_db_dir, collection_name, embedding_model)
        result = rag.query(query_text, top_k=top_k)
        st.write(f"查詢時間: {result['query_time']} 秒")
        for item in result["results"]:
            col1, col2 = st.columns([1, 3])
            with col1:
                if os.path.exists(item["image_path"]):
                    st.image(item["image_path"], width=120)
            with col2:
                st.write(f"描述: {item['caption']}")
                st.write(f"分數: {item['score']:.2f}")
