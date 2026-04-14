#!/bin/bash
# 科学示意图生成示例
#
# 前置条件:
# 1. 设置 API key: export GRSAI_API_KEY='your_key' 或 export OPENROUTER_API_KEY='your_key'
# 2. Python 3.10+
# 3. pip install requests

set -e

echo "=========================================="
echo "科学示意图 - 生成示例"
echo "=========================================="
echo ""

# 检查 API key
if [ -z "$GRSAI_API_KEY" ] && [ -z "$OPENROUTER_API_KEY" ]; then
    echo "❌ Error: 未设置 API key"
    echo ""
    echo "请设置以下环境变量之一:"
    echo "  export GRSAI_API_KEY='your_key'       # GrsAI（推荐）"
    echo "  export OPENROUTER_API_KEY='your_key'   # OpenRouter（备选）"
    exit 1
fi

echo "✓ API key 已设置"
echo ""

mkdir -p figures

# 示例 1: CONSORT 流程图
echo "示例 1: CONSORT 流程图"
echo "----------------------------"
python scripts/generate_schematic_ai.py \
  "CONSORT participant flow diagram. Assessed for eligibility (n=500). Excluded (n=150). Randomized (n=350) into Treatment (n=175) and Control (n=175)." \
  -o figures/consort_example.png

echo ""

# 示例 2: 神经网络架构
echo "示例 2: 神经网络架构"
echo "----------------------------"
python scripts/generate_schematic_ai.py \
  "Transformer encoder-decoder architecture with multi-head attention, encoder on left, decoder on right" \
  -o figures/transformer_example.png \
  --model nano-banana-2

echo ""

# 示例 3: 生物通路
echo "示例 3: 信号通路"
echo "----------------------------"
python scripts/generate_schematic_ai.py \
  "MAPK signaling: EGFR → RAS → RAF → MEK → ERK → nucleus, label arrows with phosphorylation" \
  -o figures/pathway_example.png \
  --size 2K

echo ""
echo "=========================================="
echo "所有示例完成！查看 figures/ 目录"
echo "=========================================="
