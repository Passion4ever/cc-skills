#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# sk installer — one-line install for Claude Code Skills Manager
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/Passion4ever/cc-skills/main/install.sh | bash
# ============================================================================

GITHUB_USER="Passion4ever"
GITHUB_REPO="cc-skills"
GITHUB_BRANCH="main"
API_BASE="https://api.github.com/repos/${GITHUB_USER}/${GITHUB_REPO}"

RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
CYAN=$'\033[0;36m'
BOLD=$'\033[1m'
DIM=$'\033[2m'
NC=$'\033[0m'

info() { printf '%s\n' "${CYAN}[sk]${NC} $*"; }
ok()   { printf '%s\n' "${GREEN}[sk]${NC} $*"; }
err()  { printf '%s\n' "${RED}[sk]${NC} $*" 1>&2; }

# Determine install directory
INSTALL_DIR=""
for dir in "$HOME/.local/bin" "/usr/local/bin"; do
    if [[ -d "$dir" ]] && echo "$PATH" | tr ':' '\n' | grep -qx "$dir"; then
        INSTALL_DIR="$dir"
        break
    fi
done

if [[ -z "$INSTALL_DIR" ]]; then
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
fi

INSTALL_PATH="${INSTALL_DIR}/sk"

info "正在下载 sk..."
if curl -fsSL -H "Accept: application/vnd.github.v3.raw" "${API_BASE}/contents/sk?ref=${GITHUB_BRANCH}" -o "$INSTALL_PATH"; then
    chmod +x "$INSTALL_PATH"
    ok "sk 已安装到 ${BOLD}${INSTALL_PATH}${NC}"
else
    err "下载失败，请检查网络"
    exit 1
fi

# Check if install dir is in PATH
if ! echo "$PATH" | tr ':' '\n' | grep -qx "$INSTALL_DIR"; then
    printf '%s\n' ""
    printf '%s\n' "${DIM}提示: ${INSTALL_DIR} 不在 PATH 中，请添加:${NC}"
    printf '%s\n' ""
    printf '%s\n' "  export PATH=\"${INSTALL_DIR}:\$PATH\""
    printf '%s\n' ""
    printf '%s\n' "${DIM}将上面这行加入 ~/.bashrc 或 ~/.zshrc${NC}"
fi

# Ensure ~/.claude/skills exists
mkdir -p "$HOME/.claude/skills"

printf '%s\n' ""
printf '%s\n' "${BOLD}快速开始:${NC}"
printf '%s\n' "  sk list               查看所有可用 skills"
printf '%s\n' "  sk i <name>           安装单个 skill"
printf '%s\n' "  sk i -a               安装所有 skills"
printf '%s\n' "  sk -h                 查看完整帮助"
printf '%s\n' ""
