#!/usr/bin/env python3
"""
科学示意图生成器 — 使用 Nano Banana 系列模型。

支持两个 API 供应商：
  1. GrsAI（默认）— 直连 Nano Banana API
  2. OpenRouter（备选）— 通过 Google 模型名调用

生成后由 Claude 交互式审查，不依赖 Gemini。

环境变量:
  GRSAI_API_KEY       GrsAI API key（优先）
  GRSAI_HOST          GrsAI host，默认 https://grsai.dakka.com.cn（国内）
                      海外用 https://grsaiapi.com
  OPENROUTER_API_KEY  OpenRouter API key（备选）

用法:
  python generate_schematic_ai.py "Transformer 架构图" -o figures/transformer.png
  python generate_schematic_ai.py "MAPK 信号通路" -o figures/mapk.png --model nano-banana-pro
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)


# GrsAI 可用模型
GRSAI_MODELS = [
    "nano-banana-2",          # 默认
    "nano-banana-fast",
    "nano-banana",
    "nano-banana-2-cl",
    "nano-banana-2-4k-cl",
    "nano-banana-pro",
    "nano-banana-pro-vt",
    "nano-banana-pro-cl",
    "nano-banana-pro-vip",
    "nano-banana-pro-4k-vip",
]

# OpenRouter 模型映射
OPENROUTER_MODEL_MAP = {
    "nano-banana":   "google/gemini-2.5-flash-image",
    "nano-banana-2": "google/gemini-3.1-flash-image-preview",
    "nano-banana-pro": "google/gemini-3-pro-image-preview",
}

# 科学图表生成提示词模板
SCIENTIFIC_DIAGRAM_GUIDELINES = """
Create a high-quality scientific diagram with these requirements:

VISUAL QUALITY:
- Clean white or light background
- High contrast for readability and printing
- Professional, publication-ready appearance
- Adequate spacing between elements

TYPOGRAPHY:
- Clear, readable sans-serif fonts
- Minimum 10pt font size for all labels
- Consistent font sizes throughout
- No overlapping text

SCIENTIFIC STANDARDS:
- Accurate representation of concepts
- Clear labels for all components
- Standard scientific notation and symbols
- Include units where applicable

ACCESSIBILITY:
- Colorblind-friendly color palette (Okabe-Ito)
- Works well in grayscale

LAYOUT:
- Logical flow (left-to-right or top-to-bottom)
- Clear visual hierarchy
- Balanced composition

IMPORTANT:
- Do NOT include figure numbers ("Figure 1:", "Fig. 1")
- Do NOT add captions — figure numbers and captions are added in the document
"""


class GrsAIProvider:
    """GrsAI 图像生成供应商"""

    def __init__(self, api_key: str, host: str = None, verbose: bool = False):
        self.api_key = api_key
        self.host = host or os.getenv("GRSAI_HOST", "https://grsai.dakka.com.cn")
        self.verbose = verbose

    def _log(self, msg: str):
        if self.verbose:
            print(f"[{time.strftime('%H:%M:%S')}] {msg}")

    def generate(self, prompt: str, model: str = "nano-banana-2",
                 aspect_ratio: str = "auto", image_size: str = "1K",
                 reference_urls: list = None) -> Optional[bytes]:
        """
        调用 GrsAI 绘画接口生成图片。

        Returns:
            图片 bytes 或 None
        """
        url = f"{self.host}/v1/draw/nano-banana"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        payload = {
            "model": model,
            "prompt": prompt,
            "aspectRatio": aspect_ratio,
            "imageSize": image_size,
            "shutProgress": True,  # 直接返回最终结果
        }
        if reference_urls:
            payload["urls"] = reference_urls

        self._log(f"请求 GrsAI ({model})...")
        self._log(f"Host: {self.host}")

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=180, stream=True)

            if response.status_code != 200:
                self._log(f"HTTP {response.status_code}: {response.text[:500]}")
                return None

            # 解析 stream 响应，获取最终结果
            result_data = None
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if data.get("status") == "succeeded" and data.get("results"):
                        result_data = data
                        break
                    elif data.get("status") == "failed":
                        self._log(f"生成失败: {data.get('failure_reason', 'unknown')}")
                        return None
                except json.JSONDecodeError:
                    continue

            if not result_data or not result_data.get("results"):
                self._log("未获取到结果")
                return None

            # 下载图片
            image_url = result_data["results"][0].get("url", "")
            if not image_url:
                self._log("结果中无图片 URL")
                return None

            self._log(f"下载图片: {image_url[:80]}...")
            img_response = requests.get(image_url, timeout=60)
            if img_response.status_code == 200:
                self._log(f"✓ 图片下载完成 ({len(img_response.content)} bytes)")
                return img_response.content
            else:
                self._log(f"图片下载失败: HTTP {img_response.status_code}")
                return None

        except requests.exceptions.Timeout:
            self._log("请求超时 (180s)")
            return None
        except Exception as e:
            self._log(f"请求异常: {e}")
            return None


class OpenRouterProvider:
    """OpenRouter 图像生成供应商（备选）"""

    def __init__(self, api_key: str, verbose: bool = False):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.verbose = verbose

    def _log(self, msg: str):
        if self.verbose:
            print(f"[{time.strftime('%H:%M:%S')}] {msg}")

    def generate(self, prompt: str, model: str = "nano-banana-2",
                 **kwargs) -> Optional[bytes]:
        """通过 OpenRouter 生成图片"""
        or_model = OPENROUTER_MODEL_MAP.get(model)
        if not or_model:
            self._log(f"OpenRouter 不支持模型: {model}，可用: {list(OPENROUTER_MODEL_MAP.keys())}")
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": or_model,
            "messages": [{"role": "user", "content": prompt}],
            "modalities": ["image", "text"],
        }

        self._log(f"请求 OpenRouter ({or_model})...")

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers, json=payload, timeout=120
            )
            if response.status_code != 200:
                self._log(f"HTTP {response.status_code}: {response.text[:500]}")
                return None

            data = response.json()
            choices = data.get("choices", [])
            if not choices:
                return None

            message = choices[0].get("message", {})

            # 从 images 字段提取
            images = message.get("images", [])
            if images:
                first = images[0]
                if isinstance(first, dict) and first.get("type") == "image_url":
                    url = first.get("image_url", {})
                    if isinstance(url, dict):
                        url = url.get("url", "")
                    if url and "base64," in url:
                        b64 = url.split(",", 1)[1].replace("\n", "").replace("\r", "")
                        return base64.b64decode(b64)

            # 从 content 字段提取
            content = message.get("content", "")
            if isinstance(content, str) and "data:image" in content:
                import re
                match = re.search(r'data:image/[^;]+;base64,([A-Za-z0-9+/=\s]+)', content, re.DOTALL)
                if match:
                    b64 = match.group(1).replace("\n", "").replace("\r", "").replace(" ", "")
                    return base64.b64decode(b64)

            self._log("响应中未找到图片数据")
            return None

        except Exception as e:
            self._log(f"请求异常: {e}")
            return None


def get_provider(api_key: str = None, verbose: bool = False):
    """根据环境变量自动选择 API 供应商"""
    # 优先 GrsAI
    grsai_key = api_key or os.getenv("GRSAI_API_KEY")
    if grsai_key:
        return GrsAIProvider(grsai_key, verbose=verbose), "GrsAI"

    # 备选 OpenRouter
    or_key = os.getenv("OPENROUTER_API_KEY")
    if or_key:
        return OpenRouterProvider(or_key, verbose=verbose), "OpenRouter"

    return None, None


def generate(prompt: str, output_path: str, model: str = "nano-banana-2",
             aspect_ratio: str = "auto", image_size: str = "1K",
             api_key: str = None, verbose: bool = False) -> bool:
    """
    生成科学示意图。

    Args:
        prompt: 图表描述
        output_path: 输出路径
        model: 模型名称
        aspect_ratio: 宽高比
        image_size: 图片尺寸 (1K/2K/4K)
        api_key: API key（可选）
        verbose: 详细输出

    Returns:
        是否成功
    """
    provider, provider_name = get_provider(api_key, verbose)
    if not provider:
        print("Error: 未找到 API key")
        print("请设置以下环境变量之一:")
        print("  export GRSAI_API_KEY='your_key'       # GrsAI（推荐）")
        print("  export OPENROUTER_API_KEY='your_key'   # OpenRouter（备选）")
        return False

    # 拼接科学图表指南 + 用户 prompt
    full_prompt = f"{SCIENTIFIC_DIAGRAM_GUIDELINES}\n\nUSER REQUEST: {prompt}"

    print(f"\n{'='*50}")
    print(f"生成科学示意图")
    print(f"{'='*50}")
    print(f"描述: {prompt}")
    print(f"模型: {model}")
    print(f"供应商: {provider_name}")
    print(f"输出: {output_path}")
    print(f"{'='*50}\n")

    print("正在生成...")
    image_data = provider.generate(
        prompt=full_prompt,
        model=model,
        aspect_ratio=aspect_ratio,
        image_size=image_size,
    )

    if not image_data:
        print("✗ 生成失败")
        return False

    # 保存图片
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        f.write(image_data)

    print(f"✓ 已保存: {output_path} ({len(image_data)} bytes)")
    print(f"\n提示: 请查看生成的图片，如需调整可以告诉 Claude 具体修改意见。")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="生成科学示意图（Nano Banana）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
可用模型 (GrsAI):
  {', '.join(GRSAI_MODELS)}

可用模型 (OpenRouter):
  {', '.join(f'{k} -> {v}' for k, v in OPENROUTER_MODEL_MAP.items())}

环境变量:
  GRSAI_API_KEY       GrsAI API key（推荐）
  GRSAI_HOST          GrsAI host（默认国内直连）
                      海外: https://grsaiapi.com
                      国内: https://grsai.dakka.com.cn
  OPENROUTER_API_KEY  OpenRouter API key（备选）

示例:
  python generate_schematic_ai.py "Transformer 架构图" -o transformer.png
  python generate_schematic_ai.py "蛋白质结构" -o protein.png --model nano-banana-pro
  python generate_schematic_ai.py "流程图" -o flow.png --size 2K --ratio 16:9
        """
    )

    parser.add_argument("prompt", help="图表描述")
    parser.add_argument("-o", "--output", required=True, help="输出路径")
    parser.add_argument("--model", default="nano-banana-2",
                        help=f"模型 (默认: nano-banana-2)")
    parser.add_argument("--ratio", default="auto",
                        help="宽高比: auto/1:1/16:9/9:16/4:3 等 (默认: auto)")
    parser.add_argument("--size", default="1K",
                        choices=["1K", "2K", "4K"], help="图片尺寸 (默认: 1K)")
    parser.add_argument("--api-key", help="API key")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")

    args = parser.parse_args()

    success = generate(
        prompt=args.prompt,
        output_path=args.output,
        model=args.model,
        aspect_ratio=args.ratio,
        image_size=args.size,
        api_key=args.api_key,
        verbose=args.verbose,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
