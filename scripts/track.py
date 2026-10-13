#!/usr/bin/env python3
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR = REPO_ROOT / "solutions"
README_FILE = REPO_ROOT / "README.md"

LANG_EXT_MAP = {
    ".go": "Go",
    ".rs": "Rust",
    ".py": "Python3",
    ".cpp": "C++",
    ".c": "C",
    ".java": "Java",
    ".js": "JavaScript",
    ".ts": "TypeScript",
}

def format_title(slug: str) -> str:
    words = slug.split("-")
    capitalized = []
    for w in words:
        if w.lower() in {"and", "or", "to", "in", "of", "a", "an", "the", "for"}:
            capitalized.append(w.lower())
        else:
            capitalized.append(w.capitalize())
    if capitalized:
        capitalized[0] = capitalized[0].capitalize()
    return " ".join(capitalized)

def collect_solutions():
    solutions = []
    if not SOLUTIONS_DIR.exists():
        return solutions

    pattern = re.compile(r"^(\d+)\.(.+?)(\.[^.]+)?(\.[a-zA-Z0-9]+)$")

    for entry in sorted(SOLUTIONS_DIR.iterdir()):
        if not entry.is_file():
            continue
        match = pattern.match(entry.name)
        if match:
            num = int(match.group(1))
            slug = match.group(2)
            ext = match.group(4)
            lang = LANG_EXT_MAP.get(ext, ext.lstrip("."))
            title = format_title(slug)
            rel_path = f"solutions/{entry.name}"
            solutions.append({
                "number": num,
                "title": title,
                "slug": slug,
                "lang": lang,
                "file": entry.name,
                "rel_path": rel_path,
            })
    solutions.sort(key=lambda s: s["number"])
    return solutions

def render_readme(solutions):
    total = len(solutions)
    lines = [
        "# LeetCode Solutions",
        "",
        "Personal repository for LeetCode solutions solved using `leetcode.nvim` in Neovim.",
        "",
        f"**Total Solved:** {total}",
        "",
        "## Solutions",
        "",
        "| # | Title | Language | Solution |",
        "|---|---|---|---|",
    ]

    if not solutions:
        lines.append("| - | No solutions yet | - | - |")
    else:
        for s in solutions:
            url = f"https://leetcode.com/problems/{s['slug']}/"
            title_link = f"[{s['title']}]({url})"
            code_link = f"[`{s['file']}`]({s['rel_path']})"
            lines.append(f"| {s['number']} | {title_link} | {s['lang']} | {code_link} |")

    lines.append("")
    lines.append("## Tracking & Sync")
    lines.append("")
    lines.append("Run the tracking script to regenerate this table:")
    lines.append("```bash")
    lines.append("python3 scripts/track.py")
    lines.append("```")
    lines.append("")
    lines.append("To automatically stage, commit, and push:")
    lines.append("```bash")
    lines.append("python3 scripts/track.py --push")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)

def update_readme():
    solutions = collect_solutions()
    content = render_readme(solutions)
    README_FILE.write_text(content, encoding="utf-8")
    print(f"Updated README.md with {len(solutions)} solution(s).")

def git_sync(commit_msg: str = None, push: bool = False):
    update_readme()
    subprocess.run(["git", "-C", str(REPO_ROOT), "add", "solutions", "README.md"], check=True)
    status = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True
    )
    if not status.stdout.strip():
        print("No changes to commit.")
        return

    if not commit_msg:
        commit_msg = "Update LeetCode solutions and progress"
    subprocess.run(["git", "-C", str(REPO_ROOT), "commit", "-m", commit_msg], check=True)
    print(f"Committed changes: {commit_msg}")

    if push:
        subprocess.run(["git", "-C", str(REPO_ROOT), "push"], check=True)
        print("Pushed changes to remote repository.")

def main():
    push = "--push" in sys.argv
    commit = "--commit" in sys.argv or push
    msg = None
    if "--commit" in sys.argv:
        idx = sys.argv.index("--commit")
        if idx + 1 < len(sys.argv) and not sys.argv[idx + 1].startswith("--"):
            msg = sys.argv[idx + 1]

    if commit:
        git_sync(commit_msg=msg, push=push)
    else:
        update_readme()

if __name__ == "__main__":
    main()
