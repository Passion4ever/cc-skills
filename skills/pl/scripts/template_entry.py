#!/usr/bin/env python3
"""
入口脚本模板

用法:
    python scripts/xxx.py --config configs/xxx.yaml
    python scripts/xxx.py --config configs/xxx.yaml --model.lr=1e-3
    python scripts/xxx.py --config configs/xxx.yaml --ckpt_path runs/.../last.ckpt
"""

from lightning.pytorch.cli import LightningCLI
from src.models.xxx import MyModel
from src.data.xxx import MyDataModule


def main():
    cli = LightningCLI(
        MyModel,
        MyDataModule,
        parser_kwargs={
            "parser_mode": "omegaconf",   # 启用 ${} 变量插值
        },
    )
    # LightningCLI 默认会将完整 config 保存到 default_root_dir/config.yaml


if __name__ == "__main__":
    main()
