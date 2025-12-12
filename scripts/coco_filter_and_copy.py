import os
import shutil
import json
from pycocotools.coco import COCO

# COCO annotation file path (update as needed)
ANNOTATION_PATH = "path/to/instances_train2017.json"
IMAGE_DIR = "path/to/train2017"
OUTPUT_DIR = "data/images"

# Query mapping: COCO category names
QUERY_CATEGORIES = {
    "有人的圖片": ["person"],
    "室外場景": ["outdoor"],  # COCO does not have "outdoor", use scene or location info if available
    "夜晚拍攝的照片": [],      # COCO does not have "night", use metadata if available
    "門或入口": ["door"],      # "door" may not exist, use "window"/"building"/"entrance" if needed
    "有車輛的圖片": ["car", "bus", "truck", "train", "motorcycle", "bicycle"]
}

def filter_images(coco, categories):
    cat_ids = coco.getCatIds(catNms=categories)
    img_ids = coco.getImgIds(catIds=cat_ids)
    return set(img_ids)

def main():
    coco = COCO(ANNOTATION_PATH)
    selected_img_ids = set()
    for query, cats in QUERY_CATEGORIES.items():
        if cats:
            img_ids = filter_images(coco, cats)
            print(f"{query}: {len(img_ids)} images")
            selected_img_ids.update(img_ids)
        else:
            print(f"{query}: 無法直接用 COCO category 過濾，請手動標記或用 metadata 過濾")
    # Copy images
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for img_id in selected_img_ids:
        img_info = coco.loadImgs(img_id)[0]
        src_path = os.path.join(IMAGE_DIR, img_info['file_name'])
        dst_path = os.path.join(OUTPUT_DIR, img_info['file_name'])
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
    print(f"已複製 {len(selected_img_ids)} 張圖片到 {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
