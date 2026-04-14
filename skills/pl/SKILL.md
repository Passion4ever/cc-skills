---
version: 1.0.0
name: pl
author: Passion4ever
description: |
  PyTorch Lightning 项目规范。使用 LightningCLI + OmegaConf + WandB 的标准训练框架。
  TRIGGER when: user asks to write/modify any training-related code or config;
  user mentions LightningModule, DataModule, LightningCLI, Trainer, dataloader, dataset;
  user mentions config, yaml, checkpoint, resume, finetune, pretrain;
  user mentions loss, optimizer, scheduler, lr, learning rate, callback, early stopping;
  user mentions wandb, logging, metrics, experiment tracking;
  user says "训练", "模型训练", "写训练代码", "配置训练", "写个dataloader", "改一下config";
  user asks to create project structure for deep learning;
  or any task involving PyTorch model training, evaluation, or inference pipeline.
---

# 深度学习训练框架规范（PyTorch Lightning + OmegaConf + WandB）

## 技术栈

- **PyTorch Lightning** — 训练框架，管理训练循环、checkpoint、early stopping、多卡、resume
- **OmegaConf + LightningCLI** — 配置管理，支持 YAML 配置 + `${}` 变量插值 + 命令行 override
- **WandB** — 实验追踪，日志目录必须在对应实验的 runs 目录下
- **Python 3.10+, PyTorch 2.x, CUDA 12.1**
- **pyproject.toml** — 包管理，开发环境用 `pip install -e .`，不使用 `sys.path.insert`

## 项目结构

```
project/
├── configs/
│   └── xxx.yaml                # 每个实验一个配置文件
├── src/
│   ├── models/
│   │   └── xxx.py              # LightningModule（模型 + 训练逻辑）
│   ├── data/
│   │   └── xxx.py              # LightningDataModule（数据加载）
│   └── utils/
│       └── xxx.py              # 工具函数（metrics、transforms 等）
├── scripts/
│   └── xxx.py                  # 入口脚本（很短，只有 CLI 调用）
├── tests/
│   └── test_xxx.py             # 单元测试
├── data/                       # 数据目录（通常是软链接到实际存储路径）
├── docs/                       # 项目文档
├── paper/                      # LaTeX 论文写作
├── runs/                       # 所有实验输出（自动生成）
│   └── {project_name}/{run_name}/
│       ├── config.yaml         # 本次运行的完整配置快照
│       ├── checkpoints/
│       │   ├── best.ckpt
│       │   └── last.ckpt
│       └── wandb/              # wandb 本地日志
└── figures/                    # 论文图表输出
```

## 核心规则

### 配置文件

- 所有超参数集中在 YAML 中，通过 LightningCLI（`parser_mode: "omegaconf"`）解析
- 顶层定义 `project_name` 和 `run_name`，通过 `${}` 插值到 `default_root_dir` 和 WandB logger
- `devices: auto`，通过 `CUDA_VISIBLE_DEVICES` 控制用哪些卡
- `precision: bf16-mixed`，不支持时退回 `16-mixed`
- 验证频率按任务选择：`check_val_every_n_epoch`（小数据集）或 `val_check_interval`（大数据集）
- ⚠️ 所有超参数值须根据具体任务调整，不要照搬模板默认值

> 完整配置模板见 `scripts/template_config.yaml`

### LightningModule

- `self.save_hyperparameters()` 必须调用
- `self.log()` 统一用 `"阶段/指标名"` 格式：`train/loss`, `val/loss`, `test/loss`
- 验证/测试指标加 `sync_dist=True`（多卡聚合）
- training_step 和 validation_step 逻辑不一定相同，不要强行合并
- 优化器和学习率调度器根据任务选择，不要固定写死
- 不要手动写 `.to(device)`、`optimizer.zero_grad()`、`loss.backward()`、`optimizer.step()`

> 完整模板见 `scripts/template_lightning_module.py`

### LightningDataModule

- `setup()` 需处理 `fit` 和 `test` 两个 stage
- 必须实现 `train_dataloader()`、`val_dataloader()`、`test_dataloader()`
- `train_dataloader` 设 `shuffle=True, drop_last=True`
- 需要自定义 batch 组装时使用 `collate_fn`（如变长序列 padding）

> 完整模板见 `scripts/template_datamodule.py`

### 入口脚本

- 每个入口脚本只负责调用 LightningCLI，保持极简
- 必须启用 `parser_mode: "omegaconf"`

> 完整模板见 `scripts/template_entry.py`

## 运行方式

```bash
# 基本训练
python scripts/xxx.py --config configs/xxx.yaml

# 命令行 override 超参数
python scripts/xxx.py --config configs/xxx.yaml --model.lr=1e-3 --trainer.max_epochs=100

# override 全局变量
python scripts/xxx.py --config configs/xxx.yaml --project_name=my-proj --run_name=exp_v2

# 从 checkpoint 恢复训练
python scripts/xxx.py --config configs/xxx.yaml --ckpt_path runs/.../last.ckpt

# 指定单卡
CUDA_VISIBLE_DEVICES=0 python scripts/xxx.py --config configs/xxx.yaml

# 指定多卡（自动 DDP）
CUDA_VISIBLE_DEVICES=0,2 python scripts/xxx.py --config configs/xxx.yaml

# 测试（用 best checkpoint 跑测试集）
python scripts/xxx.py --config configs/xxx.yaml --ckpt_path runs/.../best.ckpt test
```

## Checkpoint 与恢复

- **恢复训练**（断点续跑）：`--ckpt_path runs/.../last.ckpt`，加载全部状态（权重+优化器+epoch）
- **微调**（只要预训练权重）：在配置文件中指定 `model.init_args.pretrain_ckpt`，模型 `__init__` 内部加载
- Lightning checkpoint 包含：模型权重、优化器状态、scheduler 状态、epoch/step、超参数、回调状态
- 保存策略：`best.ckpt`（monitor 最优）+ `last.ckpt`（最新，用于恢复）

> 微调加载模板见 `scripts/template_lightning_module.py` 中的 `_load_pretrained` 方法

## WandB 规则

- `save_dir` 必须指向对应实验的 runs 目录
- `log_model: false` — 不上传 checkpoint 到 wandb
- WandB 初始化失败不应阻塞训练
- **多卡同步**：WandbLogger 默认只在 rank 0 记录，无需手动处理。`self.log()` 中验证/测试指标必须加 `sync_dist=True`
- 终端 progress bar 多卡时只在 rank 0 显示

## 日志 key 命名规范

```
train/loss          # 训练损失
train/lr            # 当前学习率（LearningRateMonitor 自动记录）
val/loss            # 验证损失
test/loss           # 测试损失
{stage}/{metric}    # 通用格式，metric 名根据任务定义
```

## 代码风格

- 中文注释，英文变量名
- PEP 8
- import 顺序：标准库 → 第三方库 → 项目模块
- 模型 `src/models/`，数据 `src/data/`，工具 `src/utils/`，脚本 `scripts/`，配置 `configs/`
