# cc-skills

Claude Code Skills 管理器，从 GitHub 仓库按需安装 skill 到 `~/.claude/skills/`。

## 安装

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
```

## 管理 sk 本身

```bash
sk self update            # 更新 sk 到最新版本
sk self uninstall         # 卸载 sk
```

## 添加新 skill

在 `skills/` 目录下创建子目录，包含 `SKILL.md` 文件：

```
skills/
└── my-skill/
    └── SKILL.md          # 需包含 version 字段
```

SKILL.md frontmatter 格式：

```yaml
---
name: my-skill
version: 1.0.0
description: ...
---
```

推送到 GitHub 后，其他电脑 `sk i my-skill` 即可安装。

## 致谢

部分 skills 参考并修改自以下项目：

- [anthropics/claude-code-skills](https://github.com/anthropics/claude-code-skills) — Claude 官方 Skills 库
- [K-Dense/scientific-agent-skills](https://github.com/K-Dense/scientific-agent-skills) — 科学领域 Agent Skills 库
