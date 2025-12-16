import importlib
import logging
import os
from typing import Any, List
from PIL import Image

def dynamic_import(module_name: str, class_name: str) -> Any:
    """動態匯入指定模組與類別，若失敗回傳 None。"""
    try:
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    except Exception as e:
        logging.warning(f"Import failed: {module_name}.{class_name} ({e})")
        return None

def get_image_list(image_dir: str) -> List[str]:
    """取得目錄下所有 JPG/PNG 圖片路徑（排序）"""
    if not os.path.isdir(image_dir):
        raise FileNotFoundError(f"Image dir not found: {image_dir}")
    files = []
    for f in os.listdir(image_dir):
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            files.append(os.path.join(image_dir, f))
    return sorted(files)

def load_image(image_path: str) -> Image.Image:
    """載入圖片，支援 JPG/PNG，錯誤時拋出例外"""
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    try:
        img = Image.open(image_path)
        if img.format not in ["JPEG", "PNG"]:
            raise ValueError(f"Unsupported image format: {img.format}")
        return img
    except Exception as e:
        raise RuntimeError(f"Failed to load image {image_path}: {e}")

def setup_logging(logfile: str = None):
    """配置日誌輸出到 console 和檔案"""
    handlers = [logging.StreamHandler()]
    if logfile:
        handlers.append(logging.FileHandler(logfile, encoding="utf-8"))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers
    )
