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

    lines.extend([
        "",
        "## Command Reference",
        "",
        "You can launch the plugin directly with `nvim leetcode.nvim` or run `:Leet` inside any Neovim session.",
        "",
        "### Essential Commands",
        "",
        "| Command | Description |",
        "|---|---|",
        "| `:Leet` or `:Leet menu` | Opens the main menu dashboard |",
        "| `:Leet exit` | Closes `leetcode.nvim` session |",
        "| `:Leet list` | Opens the problem search picker |",
        "| `:Leet daily` | Opens today's daily problem |",
        "| `:Leet random` | Opens a random problem |",
        "| `:Leet run` (or `:Leet test`) | Runs test cases on current solution |",
        "| `:Leet submit` | Submits current solution to LeetCode |",
        "| `:Leet console` | Opens console pop-up with test cases and run results |",
        "| `:Leet info` | Displays problem details and stats |",
        "| `:Leet hints` | Displays hints for the current problem |",
        "| `:Leet open` | Opens the current problem in your default web browser |",
        "| `:Leet yank` | Copies the current solution code section to your system clipboard |",
        "| `:Leet lang` | Opens picker to change programming language for current problem |",
        "| `:Leet tabs` | Opens tab switcher for all currently opened questions |",
        "",
        "### Editor & Layout Commands",
        "",
        "| Command | Description |",
        "|---|---|",
        "| `:Leet desc` or `:Leet desc toggle` | Toggles the problem description split |",
        "| `:Leet desc stats` | Toggles statistics display in the description split |",
        "| `:Leet reset` | Resets the editor code back to the initial starting template |",
        "| `:Leet last_submit` | Replaces editor code with your most recent accepted submission |",
        "| `:Leet restore` | Restores default window layout |",
        "| `:Leet inject` | Re-injects language boilerplate without altering your solution |",
        "| `:Leet fold` | Folds the imports/boilerplate section |",
        "",
        "### Account & Cache Commands",
        "",
        "| Command | Description |",
        "|---|---|",
        "| `:Leet cookie update` | Opens prompt to enter or update your LeetCode session cookie |",
        "| `:Leet cookie delete` | Logs out and deletes saved session cookie |",
        "| `:Leet cache update` | Refreshes local question list cache from LeetCode |",
        "",
        "### Filtering with Arguments",
        "",
        "You can pass arguments to `:Leet list` and `:Leet random` separated by commas:",
        "",
        "```vim",
        "\" Filter list by status and difficulty",
        ":Leet list status=todo difficulty=easy",
        ":Leet list status=notac difficulty=medium",
        "",
        "\" Pick random question by topic tag",
        ":Leet random difficulty=easy tags=array,hash-table",
        ":Leet random status=todo difficulty=medium tags=two-pointers",
        "```",
        "",
        "Valid values:",
        "- `difficulty`: `easy`, `medium`, `hard`",
        "- `status`: `todo`, `notac`, `ac`",
        "- `tags`: LeetCode topic tags such as `array`, `string`, `hash-table`, `dynamic-programming`, `tree`, `binary-search`, etc.",
        "",
        "## Keybindings & Interaction",
        "",
        "### Menu and Popups",
        "- `q`: Close/dismiss current modal, console, or menu",
        "- `<CR>`: Confirm selection in picker or dashboard",
        "",
        "### Console Pop-up Navigation",
        "When test results or testcases are open in the console pop-up:",
        "- `H`: Focus testcases window",
        "- `L`: Focus result window",
        "- `r`: Reset testcase input to default problem testcases",
        "- `U`: Use current testcase for evaluation",
        "- `q`: Close console pop-up",
        "",
        "## Tracking & Sync",
        "",
        "The [README.md](file:///home/dor/projects/leetcode-solutions/README.md) table regenerates automatically when exiting `leetcode.nvim`.",
        "",
        "To update manually:",
        "```bash",
        "python3 scripts/track.py",
        "```",
        "",
        "To update, stage, commit, and push to GitHub in one command:",
        "```bash",
        "python3 scripts/track.py --push",
        "```",
        "",
        "To provide a custom commit message:",
        "```bash",
        "python3 scripts/track.py --commit \"Solve Two Sum in Go\" --push",
        "```",
        "",
    ])
    return "\n".join(lines)

def update_readme():
    solutions = collect_solutions()
    content = render_readme(solutions)
    README_FILE.write_text(content, encoding="utf-8")
    print(f"Updated README.md with {len(solutions)} solution(s).")

def git_sync(commit_msg: str = None, push: bool = False):
    update_readme()
    subprocess.run(["git", "-C", str(REPO_ROOT), "add", "solutions", "README.md", "scripts"], check=True)
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
