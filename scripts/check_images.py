"""
檢查測試圖片品質與多樣性
"""
import os
from pathlib import Path
from PIL import Image
from collections import Counter
import sys

def check_images(image_dir: str):
    image_dir = Path(image_dir)
    if not image_dir.exists():
        print(f"❌ 目錄不存在: {image_dir}")
        return False
    image_files = list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.png"))
    print(f"\n📊 測試圖片檢查報告")
    print(f"{'='*50}")
    print(f"圖片目錄: {image_dir}")
    print(f"圖片數量: {len(image_files)}")
    if len(image_files) < 20:
        print(f"⚠️  圖片數量不足 20 張（當前: {len(image_files)}）")
    sizes = []
    formats = []
    valid_count = 0
    print(f"\n{'檔名':<20} {'格式':<10} {'尺寸':<20} {'大小':<10} {'狀態'}")
    print(f"{'-'*80}")
    for img_path in sorted(image_files):
        try:
            img = Image.open(img_path)
            size = img.size
            format_type = img.format
            file_size = os.path.getsize(img_path) / 1024
            sizes.append(size)
            formats.append(format_type)
            valid_count += 1
            status = "✅"
            if size[0] < 640 or size[1] < 480:
                status = "⚠️  解析度偏低"
            print(f"{img_path.name:<20} {format_type:<10} {size} {file_size:>6.1f}KB {status}")
        except Exception as e:
            print(f"{img_path.name:<20} {'N/A':<10} {'N/A':<20} {'N/A':<10} ❌ 損壞: {e}")
    print(f"\n{'='*50}")
    print(f"✅ 有效圖片: {valid_count}/{len(image_files)}")
    print(f"📊 格式分布: {dict(Counter(formats))}")
    if sizes:
        avg_width = sum(s[0] for s in sizes) / len(sizes)
        avg_height = sum(s[1] for s in sizes) / len(sizes)
        print(f"📐 平均解析度: {avg_width:.0f}x{avg_height:.0f}")
    print(f"\n💡 建議：")
    if len(image_files) < 20:
        print(f"  - 補充 {20 - len(image_files)} 張圖片")
    if valid_count < len(image_files):
        print(f"  - 修復或替換 {len(image_files) - valid_count} 張損壞圖片")
    return valid_count >= 20

if __name__ == "__main__":
    image_dir = sys.argv[1] if len(sys.argv) > 1 else "data/images"
    success = check_images(image_dir)
    sys.exit(0 if success else 1)
