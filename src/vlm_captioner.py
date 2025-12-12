import os
import time
import base64
from typing import List, Dict
from datetime import datetime
from openai import OpenAI, OpenAIError
from tqdm import tqdm
import imghdr

CAPTION_PROMPT = (
    "請用一句話描述這張圖片的主要內容，包括：\n"
    "1. 畫面中的人物或物體\n"
    "2. 正在進行的動作或行為\n"
    "3. 場景特徵（室內/室外、時間、地點）\n\n"
    "請用繁體中文回答，50字以內。"
)

class VLMCaptioner:
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_caption(self, image_path: str) -> dict:
        image_id = os.path.splitext(os.path.basename(image_path))[0]
        for attempt in range(3):
            try:
                with open(image_path, "rb") as img_file:
                    img_bytes = img_file.read()
                    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
                img_type = imghdr.what(image_path)
                if img_type == "png":
                    mime_type = "image/png"
                else:
                    mime_type = "image/jpeg"
                payload = {
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": CAPTION_PROMPT},
                                {
                                    "type": "image_url",
                                    "image_url": f"data:{mime_type};base64,{img_base64}"
                                }
                            ]
                        }
                    ],
                    "max_tokens": 100,
                    "temperature": 0.2,
                }
                response = self.client.chat.completions.create(**payload)
                print("[DEBUG] OpenAI response:", response)
                message = response.choices[0].message
                if message and message.content:
                    caption = message.content.strip()
                else:
                    caption = "[ERROR] No caption returned"
                return {
                    "image_id": image_id,
                    "image_path": image_path,
                    "caption": caption,
                    "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z"
                }
            except OpenAIError as e:
                if attempt < 2:
                    time.sleep(2)
                else:
                    return {
                        "image_id": image_id,
                        "image_path": image_path,
                        "caption": f"[ERROR] {e}",
                        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z"
                    }
            except Exception as e:
                if attempt < 2:
                    time.sleep(2)
                else:
                    return {
                        "image_id": image_id,
                        "image_path": image_path,
                        "caption": f"[ERROR] {e}",
                        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z"
                    }
            time.sleep(1.5)  # Rate limiting

        # Fallback if all retries fail (should not reach here)
        return {
            "image_id": image_id,
            "image_path": image_path,
            "caption": "[ERROR] Unknown error",
            "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z"
        }

    def batch_generate(self, image_paths: List[str]) -> List[dict]:
        results = []
        for path in tqdm(image_paths, desc="生成描述"):
            results.append(self.generate_caption(path))
            time.sleep(1.5)  # Rate limiting
        return results
