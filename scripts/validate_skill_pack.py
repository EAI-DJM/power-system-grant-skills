#!/usr/bin/env python3
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_HEADINGS = [
    "## 适用范围与触发条件",
    "## 共通约束",
    "## 所需输入",
    "## 执行步骤",
    "## 输出格式",
    "## 核查标准",
    "## 注意事项",
]


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors = []
    lines = text.splitlines()
    if len(lines) > 100:
        errors.append(f"超过100行: {len(lines)}")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        errors.append("缺少有效frontmatter")
    else:
        frontmatter = match.group(1)
        if not re.search(r"^name:\s*[a-z0-9-]+$", frontmatter, re.M):
            errors.append("name缺失或格式错误")
        desc = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
        if not desc:
            errors.append("description缺失")
        elif "Use when" not in desc.group(1):
            errors.append("description缺少触发条件")
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"缺少章节: {heading}")
    return errors


def main() -> int:
    skill_files = sorted(ROOT.glob("*/SKILL.md"))
    if not skill_files:
        print("未找到SKILL.md", file=sys.stderr)
        return 1
    failed = False
    for path in skill_files:
        errors = validate(path)
        if errors:
            failed = True
            print(f"FAIL {path.relative_to(ROOT)}")
            for error in errors:
                print(f"  {error}")
        else:
            print(f"PASS {path.relative_to(ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
