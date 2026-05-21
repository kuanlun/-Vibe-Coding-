"""国内环境推荐：python run.py（无需单独安装 uvicorn 命令）"""
import sys
from pathlib import Path

import uvicorn

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> None:
    reload = "--reload" in sys.argv or "-r" in sys.argv
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=reload,
    )


if __name__ == "__main__":
    main()
