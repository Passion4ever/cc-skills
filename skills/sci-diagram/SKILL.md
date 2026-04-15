---
version: 2.0.1
name: sci-diagram
author: Passion4ever
description: |
  生成出版级科学示意图。使用 Nano Banana 系列 AI 模型生成，Claude 交互式审查。
  TRIGGER when: user asks to create/draw/generate scientific diagrams, architecture diagrams, flowcharts;
  user mentions "画图", "示意图", "架构图", "流程图", "通路图", "模型架构";
  user mentions neural network architecture, system diagram, biological pathway, circuit diagram;
  user asks for figure, schematic, or diagram for a paper/poster/presentation;
  or any task involving scientific visual content creation.
  DO NOT TRIGGER for data plots (use sci-plot instead).
---

# 科学示意图生成（Nano Banana AI + Claude 审查）

## 概述

用自然语言描述你想要的图，Nano Banana AI 生成，Claude 审查质量并交互式改进。

**工作流程:**
1. 描述你要什么图 → Nano Banana 生成
2. Claude 查看生成结果 → 给出评审意见
3. 不满意 → 告诉 Claude 哪里要改 → 重新生成
4. 满意 → 完成

**不需要编码、模板或手动绘图。**

## 配置

设置 API key（二选一）：

```bash
# 方式 1: GrsAI（推荐，直连 Nano Banana API）
export GRSAI_API_KEY='your_key'
# 国内直连（默认）：
export GRSAI_HOST='https://grsai.dakka.com.cn'
# 海外：
export GRSAI_HOST='https://grsaiapi.com'

# 方式 2: OpenRouter（备选）
export OPENROUTER_API_KEY='your_key'
```

## 可用模型

### GrsAI（全部模型）

| 模型 | 说明 |
|---|---|
| `nano-banana-2`（默认） | 第二代，质量均衡 |
| `nano-banana-fast` | 快速生成 |
| `nano-banana` | 标准版 |
| `nano-banana-2-cl` | 第二代 CL |
| `nano-banana-2-4k-cl` | 第二代 4K |
| `nano-banana-pro` | Pro 高质量 |
| `nano-banana-pro-vt` | Pro VT |
| `nano-banana-pro-cl` | Pro CL |
| `nano-banana-pro-vip` | Pro VIP |
| `nano-banana-pro-4k-vip` | Pro 4K VIP |

### OpenRouter（部分模型）

| Nano Banana 名 | OpenRouter 模型 ID |
|---|---|
| nano-banana | google/gemini-2.5-flash-image |
| nano-banana-2 | google/gemini-3.1-flash-image-preview |
| nano-banana-pro | google/gemini-3-pro-image-preview |

## 使用方式

Claude 会自动调用脚本生成图片，你只需要用自然语言描述：

> "帮我画一个 Transformer encoder-decoder 架构图"
> "画一个 MAPK 信号通路图，从 EGFR 到基因转录"
> "生成一个 CONSORT 流程图"

### 脚本直接调用（高级）

```bash
# 基本用法
python scripts/generate_schematic_ai.py "描述" -o output.png

# 指定模型
python scripts/generate_schematic_ai.py "描述" -o output.png --model nano-banana-pro

# 指定尺寸和比例
python scripts/generate_schematic_ai.py "描述" -o output.png --size 2K --ratio 16:9
```

参数说明见 `scripts/generate_schematic_ai.py --help`

## Prompt 编写技巧

**好的 prompt（具体、详细）:**
- "Transformer encoder-decoder architecture with multi-head attention, showing encoder stack on left, decoder on right, cross-attention connections"
- "CONSORT flowchart: 500 screened → 150 excluded → 350 randomized → treatment (175) vs control (175)"
- "MAPK signaling: EGFR → RAS → RAF → MEK → ERK → nucleus, label each arrow with phosphorylation"

**差的 prompt（模糊）:**
- "画一个流程图"
- "神经网络"
- "通路图"

**关键要素:**
- **类型**: 流程图、架构图、通路图、电路图等
- **组件**: 具体包含哪些元素
- **流向**: 从左到右、从上到下
- **标签**: 需要标注什么
- **风格**: 简约、详细、配色要求

## 质量标准（Claude 审查时关注）

- 科学准确性 — 概念、符号、关系是否正确
- 清晰可读 — 一眼能看懂，层次分明
- 标签完整 — 所有元素都有标注，字体可读
- 布局合理 — 逻辑流向，无重叠
- 出版质量 — 干净专业，适合论文/海报

## 与其他 skill 配合

- **sci-plot** — 数据图（折线、柱状、热力图），sci-diagram 画概念图
- **sci-writing** — 论文写作，调用 sci-diagram 生成 Figure
- **latex-posters / pptx** — 海报/演示，嵌入生成的图

## 资源

- `references/best_practices.md` — 出版标准和可访问性指南
- `references/QUICK_REFERENCE.md` — 快速参考
