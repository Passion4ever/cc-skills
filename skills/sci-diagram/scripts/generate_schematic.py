#!/usr/bin/env python3
"""
科学示意图生成入口脚本。

简化调用，自动检测 API key 并转发到核心生成脚本。

用法:
    python generate_schematic.py "Transformer 架构图" -o figures/transformer.png
    python generate_schematic.py "MAPK 通路" -o figures/mapk.png --model nano-banana-pro
    python generate_schematic.py "流程图" -o figures/flow.png --size 2K
"""

import subprocess
import sys
from pathlib import Path


def main():
    script_dir = Path(__file__).parent
    ai_script = script_dir / "generate_schematic_ai.py"

    if not ai_script.exists():
        print(f"Error: {ai_script} not found")
        sys.exit(1)

    # 直接转发所有参数
    cmd = [sys.executable, str(ai_script)] + sys.argv[1:]
    result = subprocess.run(cmd, check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
