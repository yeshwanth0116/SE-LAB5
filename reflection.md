# Lab 5 Reflection — Static Code Analysis

1) How difficult were the fixes?

The fixes were straightforward for the issues flagged by the analyzers. Most problems were small and low-risk: replacing a mutable default with `None`, adding explicit exception handling, using `with` for file I/O, removing `eval`, and applying simple input-type validation. The largest effort was ensuring function signatures and docstrings followed style guidelines while preserving behavior. Overall, the work took a few iterative edits and 2–3 re-runs of the tools to reach a clean state.

2) Any false positives or noisy warnings?

There were a number of style and naming warnings (missing docstrings, naming conventions). These are not false positives — they are stylistic — but they can be noisy in a short educational script. Bandit reported `eval` (legitimate) and the bare except (legitimate). Pylint suggested additional improvements (module docstring, naming). Flake8 gave many blank-line/style issues that were easy to fix. No high-confidence false positives were encountered; most flagged items were actionable.

3) How to integrate these tools into a development workflow?

- Add the tools as dev dependencies and run them in CI (GitHub Actions). Create a workflow that runs flake8/pylint/bandit on push/PR and fails on new critical issues.
- For local developer ergonomics, add pre-commit hooks (pre-commit framework) to run flake8 and bandit quickly on changed files and optionally run pylint on staged files.
- Configure a baseline file or ignore list for legacy code so the team can focus on new issues.

4) How did the changes improve code quality?

- Security: removing `eval` and explicit exception handling reduced attack surface and improved observability.
- Reliability: validated inputs and used `.get()` with defaults so the module no longer raises KeyError from simple lookups.
- Maintainability: clearer function names, docstrings, and logging make the code easier to read and debug.
- Portability: specifying file encodings reduces platform-dependent behavior.

Files changed:

- `inventorysystem.py` — fixed issues (mutable default, bare except, eval, file handling, type checks, logging, naming and docstrings).
- `issues_table.md` — documented the identified issues and fixes.
- `reflection.md` — this file.

Quick reproduction steps I ran in the Codespace (already executed here):

```bash
# ensure venv python is used (devcontainer)
/workspaces/SE-LAB5/.venv/bin/python -m pip install pylint bandit flake8
/workspaces/SE-LAB5/.venv/bin/python -m pylint /workspaces/SE-LAB5/inventorysystem.py
/workspaces/SE-LAB5/.venv/bin/python -m bandit -r /workspaces/SE-LAB5/inventorysystem.py -f txt -o banditreport.txt
/workspaces/SE-LAB5/.venv/bin/python -m flake8 /workspaces/SE-LAB5/inventorysystem.py > flake8report.txt
```

Final analyzer results from my run:

- Pylint score: 9.87/10
- Bandit: No issues identified
- Flake8: No errors

Next steps (optional): add automated CI checks and enforce a subset of these checks as pre-commit hooks to prevent regressions.
