# cc-skills

个人 Claude Code Skills 管理工具，支持按需安装、卸载、更新。

## 安装 sk

```bash
curl -fsSL https://raw.githubusercontent.com/Passion4ever/cc-skills/main/install.sh | bash
```

## 使用

```bash
sk list                   # 查看所有 skills 及版本状态
sk i <name>               # 安装单个 skill
sk i -a                   # 安装所有 skills
sk uni <name>             # 卸载单个 skill
sk uni -a                 # 卸载所有 skills
sk update <name>          # 更新单个 skill
sk update -a              # 一键更新所有
sk self update            # 更新 sk 本身
sk self uninstall         # 卸载 sk 本身
```
