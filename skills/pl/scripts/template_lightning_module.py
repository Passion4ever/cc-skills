"""
LightningModule 模板

所有超参数通过 __init__ 参数传入，由 LightningCLI 从 YAML 配置注入。
"""

import lightning.pytorch as pl
import torch
import torch.nn as nn
from lightning.pytorch.utilities import rank_zero_info


class MyModel(pl.LightningModule):
    def __init__(
        self,
        lr: float = 5e-4,
        weight_decay: float = 0.01,
        warmup_steps: int = 200,
        pretrain_ckpt: str = None,
        # ... 其他超参数根据具体任务定义
    ):
        super().__init__()
        self.save_hyperparameters()  # 自动保存所有 init 参数到 checkpoint

        # 构建网络
        self.network = ...

        # 微调场景：加载预训练权重
        if pretrain_ckpt:
            self._load_pretrained(pretrain_ckpt)

    def forward(self, x):
        return self.network(x)

    def training_step(self, batch, batch_idx):
        # 训练逻辑（可能包含 augmentation、noise injection 等训练专属操作）
        loss = ...
        self.log("train/loss", loss, prog_bar=True)
        # self.log("train/xxx", xxx)  # 其他训练指标
        return loss

    def validation_step(self, batch, batch_idx):
        # 验证逻辑（与训练逻辑不一定相同）
        loss = ...
        self.log("val/loss", loss, prog_bar=True, sync_dist=True)
        # self.log("val/xxx", xxx, sync_dist=True)  # 其他验证指标

    def test_step(self, batch, batch_idx):
        # 测试集最终评估（训练完成后用 trainer.test() 调用）
        loss = ...
        self.log("test/loss", loss, sync_dist=True)
        # self.log("test/xxx", xxx, sync_dist=True)

    def configure_optimizers(self):
        # 优化器根据任务选择，常用: AdamW, Adam, SGD
        optimizer = torch.optim.AdamW(
            self.parameters(),
            lr=self.hparams.lr,
            weight_decay=self.hparams.weight_decay,
        )
        # 学习率调度器根据任务选择，常用组合:
        # 1. CosineAnnealingLR（无 warmup）
        # 2. LinearLR + CosineAnnealingLR（带 warmup，推荐）
        # 3. ReduceLROnPlateau（根据验证指标自动调整）
        total_steps = self.trainer.estimated_stepping_batches
        warmup = torch.optim.lr_scheduler.LinearLR(
            optimizer, start_factor=0.01, total_iters=self.hparams.warmup_steps
        )
        cosine = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=total_steps - self.hparams.warmup_steps
        )
        scheduler = torch.optim.lr_scheduler.SequentialLR(
            optimizer, [warmup, cosine], milestones=[self.hparams.warmup_steps]
        )
        return {
            "optimizer": optimizer,
            "lr_scheduler": {
                "scheduler": scheduler,
                "interval": "step",
            },
        }

    def _load_pretrained(self, path):
        """加载预训练权重（只加载模型权重，不加载优化器等状态）"""
        ckpt = torch.load(path, map_location="cpu", weights_only=False)
        # Lightning checkpoint 的权重在 ckpt["state_dict"]
        # 非 Lightning checkpoint（如 HuggingFace）可能直接就是 state_dict
        state_dict = ckpt.get("state_dict", ckpt)
        # strict=False 允许新增/缺失参数
        missing, unexpected = self.network.load_state_dict(state_dict, strict=False)
        rank_zero_info(f"预训练权重加载: missing={len(missing)}, unexpected={len(unexpected)}")
