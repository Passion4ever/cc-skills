# cc-skills

个人 Claude Code Skills 管理工具，支持按需安装、卸载、更新。

## 安装 sk

```bash
curl -fsSL https://raw.githubusercontent.com/Passion4ever/cc-skills/main/install.sh | bash
```

## 使用

```bash
sk list                   # 查看所有可用 skills
sk install <name>         # 安装单个 skill
sk install -a             # 安装所有 skills
sk uninstall <name>       # 卸载单个 skill
sk uninstall -a           # 卸载所有 skills
sk check                  # 对比本地与远程版本
sk update <name>          # 更新单个 skill
sk update -a              # 一键更新所有
```

## 卸载 sk

```bash
sk self-uninstall
```
