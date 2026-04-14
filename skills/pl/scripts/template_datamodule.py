"""
LightningDataModule 模板

数据路径、划分方式等参数通过 __init__ 传入，由 LightningCLI 从 YAML 配置注入。
"""

import lightning.pytorch as pl
from torch.utils.data import DataLoader, Dataset


class MyDataModule(pl.LightningDataModule):
    def __init__(
        self,
        batch_size: int = 128,
        num_workers: int = 4,
        # ... 其他数据参数根据具体任务定义（路径、划分方式、预处理参数等）
    ):
        super().__init__()
        self.save_hyperparameters()

    def setup(self, stage=None):
        """加载数据，stage 为 'fit', 'validate', 'test', 'predict'"""
        if stage in ("fit", None):
            self.train_dataset = ...
            self.val_dataset = ...
        if stage in ("test", None):
            self.test_dataset = ...

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.hparams.batch_size,
            shuffle=True,
            num_workers=self.hparams.num_workers,
            pin_memory=True,
            drop_last=True,
            # collate_fn=...,         # 需要自定义 batch 组装时启用（如变长序列 padding）
        )

    def val_dataloader(self):
        return DataLoader(
            self.val_dataset,
            batch_size=self.hparams.batch_size,
            shuffle=False,
            num_workers=self.hparams.num_workers,
            pin_memory=True,
        )

    def test_dataloader(self):
        return DataLoader(
            self.test_dataset,
            batch_size=self.hparams.batch_size,
            shuffle=False,
            num_workers=self.hparams.num_workers,
            pin_memory=True,
        )
