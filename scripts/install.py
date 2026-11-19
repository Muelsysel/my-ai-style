#!/usr/bin/env python3
"""把 agents/AGENTS.md 安装到目标仓库根目录。

规则：
- 源文件是本仓库的 agents/AGENTS.md，唯一可编辑的规约。
- 目标仓库已有的「## 5. 项目索引」整段保留，其余内容用模板覆盖。
- 目标已有 AGENTS.md 却找不到该项目索引段落时中止，确认覆盖需加 --force。
- 生成文件首行写入模板版本，--check 用它判断是否落后于源。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "agents" / "AGENTS.md"
VERSION_FILE = REPO / "VERSION"
TARGET_NAME = "AGENTS.md"

SECTION5_RE = re.compile(r"^##\s*5\.\s*项目索引[^\n]*\n", re.MULTILINE)
MARKER_RE = re.compile(r"^<!--\s*ai-style[^\n]*-->\n{0,2}", re.MULTILINE)
MARKER_LINE_RE = re.compile(r"^<!--\s*ai-style[^\n]*-->", re.MULTILINE)


def read_version() -> str:
    return VERSION_FILE.read_text("utf-8").strip()


def marker() -> str:
    return f"<!-- ai-style v{read_version()} | 源：agents/AGENTS.md，由脚本生成，勿直接修改 -->"


def strip_marker(text: str) -> str:
    return MARKER_RE.sub("", text)


def project_index(text: str) -> str | None:
    stripped = strip_marker(text)
    match = SECTION5_RE.search(stripped)
    if not match:
        return None
    return stripped[match.start() :].strip()


def render(preserved: str | None) -> str:
    stripped = strip_marker(SOURCE.read_text("utf-8")).lstrip("\n")
    match = SECTION5_RE.search(stripped)
    head = stripped[: match.start()].rstrip() if match else stripped.rstrip()
    tail = stripped[match.start() :].strip() if match else ""
    index = preserved.strip() if preserved else tail
    return f"{marker()}\n\n{head}\n\n{index}\n"


def normalize(text: str) -> str:
    text = strip_marker(text)
    text = "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").split("\n"))
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def marker_line(text: str) -> str | None:
    match = MARKER_LINE_RE.search(text)
    return match.group(0) if match else None


def is_current(old: str | None, new: str) -> bool:
    if old is None:
        return False
    return normalize(old) == normalize(new) and marker_line(old) == marker_line(new)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="把 agents/AGENTS.md 安装到目标仓库，保留目标仓库的项目索引。"
    )
    parser.add_argument("target", help="目标仓库根目录")
    parser.add_argument("--check", action="store_true", help="只检查目标是否与源一致，不写文件")
    parser.add_argument("--dry-run", action="store_true", help="只预览将要写入的内容")
    parser.add_argument("--force", action="store_true", help="目标无可识别的项目索引段落时仍覆盖")
    args = parser.parse_args()

    target_dir = Path(args.target).resolve()
    if not target_dir.is_dir():
        print(f"目标目录不存在：{target_dir}", file=sys.stderr)
        return 2

    dest = target_dir / TARGET_NAME
    old = dest.read_text("utf-8") if dest.exists() else None
    preserved = project_index(old) if old is not None else None
    new = render(preserved)

    if args.check:
        if old is None:
            print(f"缺少 {dest}，需要安装")
            return 1
        if is_current(old, new):
            print(f"一致：{dest}（模板 v{read_version()}）")
            return 0
        print(f"落后于源：{dest}（运行 python scripts/install.py {target_dir} 更新）")
        return 1

    if old is not None and preserved is None and not args.force and not args.dry_run:
        print(
            f"{dest} 已存在但没有「## 5. 项目索引」段落，为避免覆盖自定义规则已中止；确认覆盖请加 --force",
            file=sys.stderr,
        )
        return 3

    if is_current(old, new):
        print(f"已是最新：{dest}")
        return 0

    if args.dry_run:
        print(new)
        return 0

    dest.write_text(new, "utf-8", newline="\n")
    print(("更新" if old else "新建") + f"：{dest}（模板 v{read_version()}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
