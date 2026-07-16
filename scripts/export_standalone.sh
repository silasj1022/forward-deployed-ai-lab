#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${1:-../enterprise-agent-foundry-standalone}"
mkdir -p "$TARGET_DIR"
rsync -a --delete --exclude '.git' --exclude '.venv' --exclude '__pycache__' "$SOURCE_DIR/" "$TARGET_DIR/"
echo "Exported standalone project to $TARGET_DIR"
