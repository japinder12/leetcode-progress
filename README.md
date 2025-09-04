# LeetCode Progress

Track my LeetCode practice: solutions and some notes.

## Structure
- `problems/` → Code solutions organized by difficulty
  - `easy/`, `medium/`, `hard/`
- `notes/` → Patterns, approaches, and important takeaways
  - `patterns.md`, `dp.md`, `graphs.md`


## Conventions
- Naming: `problems/<difficulty>/<4-digit-id>-<problem-title>.py` (e.g., `problems/easy/0001-two-sum.py`)
- Commit per solution: `git commit -m "add 0001 Two Sum (Easy) - hashmap solution"`

## Run Tests Locally (Python)
- Create a testcase file: `tests/<id>.txt` (e.g., `tests/0001.txt`). Use Python-style assignments; blank line separates cases. Example:
  nums = [2,7,11,15]
  target = 9
  expected = [0,1]

- Run by problem id (auto-finds the solution file):
  `python tools/lc.py 0001`

- Or run by explicit path and tests:
  `python tools/lc.py problems/easy/0001-two-sum.py -t tests/0001.txt`

- Notes:
  - If `expected` is present, it checks and reports pass/fail; otherwise it just prints outputs.
  - Values must be Python literals (True/False/None, quoted strings, etc.).
  - Linked list helper: if your solution defines `ListNode`, you can write `l1 = [2,4,3]` and it auto-converts to a linked list; returned lists are printed (and compared) as plain Python lists.
