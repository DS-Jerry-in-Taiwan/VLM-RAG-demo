import os
import logging
from typing import List
from PIL import Image

SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png")

def load_image(image_path: str) -> Image.Image:
    """Load an image file, raise error if not found or unsupported format."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    ext = os.path.splitext(image_path)[1].lower()
    if ext not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported image format: {ext}")
    try:
        return Image.open(image_path)
    except Exception as e:
        raise RuntimeError(f"Failed to load image {image_path}: {e}")

def get_image_list(image_dir: str) -> List[str]:
    """Return a list of image file paths in the directory (JPG/PNG only)."""
    if not os.path.isdir(image_dir):
        raise NotADirectoryError(f"Not a directory: {image_dir}")
    files = []
    for fname in os.listdir(image_dir):
        ext = os.path.splitext(fname)[1].lower()
        if ext in SUPPORTED_FORMATS:
            files.append(os.path.join(image_dir, fname))
    return sorted(files)

def setup_logging(log_file: str = "app.log"):
    """Configure logging to output to both console and file."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # File handler
    fh = logging.FileHandler(log_file)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
