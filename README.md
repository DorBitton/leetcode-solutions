# LeetCode Solutions

Personal repository for LeetCode solutions solved using `leetcode.nvim` in Neovim.

**Total Solved:** 1

## Solutions

| # | Title | Language | Solution |
|---|---|---|---|
| 1 | [Two Sum](https://leetcode.com/problems/two-sum/) | Go | [`1.two-sum.go`](solutions/1.two-sum.go) |

## First Time Setup: Authentication

LeetCode requires your session cookie to load problems and run submissions:

1. Log in to https://leetcode.com in your browser.
2. Open Developer Tools (`F12`), go to the Application or Storage tab, and select Cookies -> `https://leetcode.com`.
3. Copy the values of `LEETCODE_SESSION` and `csrftoken` in this format:
   ```text
   LEETCODE_SESSION=your_session_value; csrftoken=your_csrf_token;
   ```
4. In Neovim, run `:Leet` and press `s` (or run `:Leet cookie update`), paste the cookie string, and press Enter.

## Command Reference

You can launch the plugin directly with `nvim leetcode.nvim` or run `:Leet` inside any Neovim session.

### Essential Commands

| Command | Description |
|---|---|
| `:Leet` or `:Leet menu` | Opens the main menu dashboard |
| `:Leet exit` | Closes `leetcode.nvim` session |
| `:Leet list` | Opens the problem search picker |
| `:Leet daily` | Opens today's daily problem |
| `:Leet random` | Opens a random problem |
| `:Leet run` (or `:Leet test`) | Runs test cases on current solution |
| `:Leet submit` | Submits current solution to LeetCode |
| `:Leet console` | Opens console pop-up with test cases and run results |
| `:Leet info` | Displays problem details and stats |
| `:Leet hints` | Displays hints for the current problem |
| `:Leet open` | Opens the current problem in your default web browser |
| `:Leet yank` | Copies the current solution code section to your system clipboard |
| `:Leet lang` | Opens picker to change programming language for current problem |
| `:Leet tabs` | Opens tab switcher for all currently opened questions |

### Editor & Layout Commands

| Command | Description |
|---|---|
| `:Leet desc` or `:Leet desc toggle` | Toggles the problem description split |
| `:Leet desc stats` | Toggles statistics display in the description split |
| `:Leet reset` | Resets the editor code back to the initial starting template |
| `:Leet last_submit` | Replaces editor code with your most recent accepted submission |
| `:Leet restore` | Restores default window layout |
| `:Leet inject` | Re-injects language boilerplate without altering your solution |
| `:Leet fold` | Folds the imports/boilerplate section |

### Account & Cache Commands

| Command | Description |
|---|---|
| `:Leet cookie update` | Opens prompt to enter or update your LeetCode session cookie |
| `:Leet cookie delete` | Logs out and deletes saved session cookie |
| `:Leet cache update` | Refreshes local question list cache from LeetCode |

### Filtering with Arguments

You can pass arguments to `:Leet list` and `:Leet random` separated by commas:

```vim
" Filter list by status and difficulty
:Leet list status=todo difficulty=easy
:Leet list status=notac difficulty=medium

" Pick random question by topic tag
:Leet random difficulty=easy tags=array,hash-table
:Leet random status=todo difficulty=medium tags=two-pointers
```

Valid values:
- `difficulty`: `easy`, `medium`, `hard`
- `status`: `todo`, `notac`, `ac`
- `tags`: LeetCode topic tags such as `array`, `string`, `hash-table`, `dynamic-programming`, `tree`, `binary-search`, etc.

## Keybindings & Interaction

### Menu and Popups
- `q`: Close/dismiss current modal, console, or menu
- `<CR>`: Confirm selection in picker or dashboard

### Console Pop-up Navigation
When test results or testcases are open in the console pop-up:
- `H`: Focus testcases window
- `L`: Focus result window
- `r`: Reset testcase input to default problem testcases
- `U`: Use current testcase for evaluation
- `q`: Close console pop-up

## Tracking & Sync

The [README.md](file:///home/dor/projects/leetcode-solutions/README.md) table regenerates automatically when exiting `leetcode.nvim`.

To update manually:
```bash
python3 scripts/track.py
```

To update, stage, commit, and push to GitHub in one command:
```bash
python3 scripts/track.py --push
```

To provide a custom commit message:
```bash
python3 scripts/track.py --commit "Solve Two Sum in Go" --push
```
