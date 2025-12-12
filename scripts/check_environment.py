"""
環境健康檢查腳本
"""
import sys
import os
from pathlib import Path
import importlib.util

def check_python_version():
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python 版本: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python 版本過低: {version.major}.{version.micro} (需要 >= 3.9)")
        return False

def check_packages():
    required = ["openai", "llama_index", "chromadb", "PIL", "dotenv", "streamlit"]
    print("\n📦 檢查套件安裝:")
    all_ok = True
    for package in required:
        spec = importlib.util.find_spec(package)
        if spec is not None:
            print(f"  ✅ {package}")
        else:
            print(f"  ❌ {package} (未安裝)")
            all_ok = False
    return all_ok

def check_env_file():
    env_path = Path(".env")
    print("\n🔐 檢查環境變數:")
    if not env_path.exists():
        print("  ❌ .env 檔案不存在")
        print("  💡 請執行: cp .env.example .env")
        return False
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key.startswith("sk-"):
        print(f"  ✅ OPENAI_API_KEY: sk-...{api_key[-4:]}")
        return True
    else:
        print("  ❌ OPENAI_API_KEY 未設置或格式錯誤")
        return False

def check_directories():
    required_dirs = ["data/images", "data/chroma_db", "logs", "src", "scripts"]
    print("\n📁 檢查目錄結構:")
    all_ok = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ⚠️  {dir_path} (不存在，將自動建立)")
            path.mkdir(parents=True, exist_ok=True)
            all_ok = False
    return all_ok

def check_api_connectivity():
    print("\n🌐 檢查 API 連線:")
    try:
        from openai import OpenAI
        from dotenv import load_dotenv
        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input="test"
        )
        print("  ✅ API 連線正常")
        return True
    except Exception as e:
        print(f"  ❌ API 連線失敗: {e}")
        return False

def main():
    print("=" * 60)
    print("🔍 Phase 1 環境健康檢查")
    print("=" * 60)
    checks = {
        "Python 版本": check_python_version(),
        "套件安裝": check_packages(),
        "環境變數": check_env_file(),
        "目錄結構": check_directories(),
        "API 連線": check_api_connectivity()
    }
    print("\n" + "=" * 60)
    print("📊 檢查結果:")
    for name, result in checks.items():
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"  {name}: {status}")
    all_passed = all(checks.values())
    print("=" * 60)
    if all_passed:
        print("\n✅ 環境檢查全部通過，可以開始測試！")
        return 0
    else:
        print("\n❌ 部分檢查失敗，請修復後再繼續")
        return 1

if __name__ == "__main__":
    sys.exit(main())
